from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "BRPAP is alive! Your business prediction engine is running in the cloud."}

@app.get("/predict")
def predict():
    # This will later do real AI
    return {"cash_forecast": [10000, 9500, 9200, 8800, 8500, 8100]}
