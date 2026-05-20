import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
import stripe

from ai_engine import forecast_cash
from rule_engine import generate_solutions
from schemas import PainPointRequest

load_dotenv()
app = FastAPI()

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)
SAMPLE_DATA_FILE = DATA_DIR / "sample_financial.csv"
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
DOMAIN_URL = os.getenv("DOMAIN_URL", "http://localhost:8000")

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

jinja_env = Environment(
    loader=FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=select_autoescape(["html", "xml"]),
)


def list_data_files():
    files = [SAMPLE_DATA_FILE] + sorted(UPLOAD_DIR.glob("*.csv"))
    seen = set()
    unique_files = []
    for f in files:
        if f.exists() and f.name not in seen:
            seen.add(f.name)
            unique_files.append(f.name)
    return unique_files


def resolve_file_path(file_name: str) -> Path:
    safe_name = Path(file_name).name
    if safe_name == SAMPLE_DATA_FILE.name:
        return SAMPLE_DATA_FILE
    candidate = UPLOAD_DIR / safe_name
    if candidate.exists() and candidate.is_file():
        return candidate
    raise HTTPException(status_code=404, detail="File not found")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    template = jinja_env.get_template("index.html")
    return HTMLResponse(template.render(request=request))


@app.get("/files")
def files(search: str | None = Query(None, description="Search filenames")):
    file_names = list_data_files()
    if search:
        search_lower = search.lower()
        file_names = [name for name in file_names if search_lower in name.lower()]
    return JSONResponse({"files": file_names})


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    filename = Path(file.filename).name
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV uploads are allowed")

    target = UPLOAD_DIR / filename
    with target.open("wb") as out_file:
        out_file.write(file.file.read())

    return {"filename": filename, "message": "Upload complete"}


@app.get("/predict")
def predict(
    file_name: str = Query(SAMPLE_DATA_FILE.name, description="CSV file name to forecast"),
    periods: int = Query(6, gt=0, le=24),
):
    try:
        path = resolve_file_path(file_name)
        forecast = forecast_cash(str(path), periods=periods)
        return {
            "source": str(path.name),
            "forecast_periods": periods,
            "forecast": forecast,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/create-checkout-session")
def create_checkout_session(request: Request):
    if not STRIPE_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Stripe secret key not configured")

    stripe.api_key = STRIPE_SECRET_KEY
    domain = DOMAIN_URL.rstrip("/")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "BRPAP Monthly Forecasting",
                            "description": "$49/month subscription for AI forecasting and business prediction",
                        },
                        "recurring": {"interval": "month"},
                        "unit_amount": 4900,
                    },
                    "quantity": 1,
                }
            ],
            success_url=f"{domain}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain}/cancel",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Stripe error: {exc}")

    return RedirectResponse(session.url, status_code=303)


@app.get("/success", response_class=HTMLResponse)
def success(request: Request):
    template = jinja_env.get_template("success.html")
    return HTMLResponse(template.render(request=request))


@app.get("/cancel", response_class=HTMLResponse)
def cancel(request: Request):
    template = jinja_env.get_template("cancel.html")
    return HTMLResponse(template.render(request=request))


@app.post("/solution")
def solution(request: PainPointRequest):
    solutions = generate_solutions(request.pain_points)
    return {"solutions": solutions}
