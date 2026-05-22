# BRPAP

BRPAP is a FastAPI-based business prediction service that now includes real time-series forecasting and Stripe payment checkout support.

## Features

- Real cash balance forecasting from sample financial CSV data using Prophet
- Upload CSV datasets to a searchable data library with metadata tracking
- Professional dashboard UI with forecast preview, dataset cards, and visual insights
- `GET /files` returns the available dataset library
- `POST /upload` accepts new CSV datasets and saves unique filenames when duplicates occur
- `/predict` endpoint supports real named data files and returns confidence bounds
- Stripe checkout integration for a $49/month subscription
- Deployment-ready with `Procfile`, `Dockerfile`, and `render.yaml`

## Local setup

1. Install dependencies:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. Configure Stripe environment values in `.env` or your shell:
   ```bash
   export STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY
   export DOMAIN_URL=http://localhost:8000
   ```

3. Start the app:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Endpoints

- `GET /files` - returns the available CSV dataset library
- `POST /upload` - uploads a new CSV file to the app library
- `GET /predict?file_name=<filename>` - returns a forecast from a selected dataset
- `GET /create-checkout-session` - redirects to Stripe Checkout for $49/month subscription
- `GET /success` - confirmation page after subscription success
- `GET /cancel` - canceled checkout page

## Sample data

The sample CSV file is located at `data/sample_financial.csv` and includes monthly cash balance history.

## Deployment

- Use `Procfile` for Heroku/Render deployment
- Use `Dockerfile` for container-based deployment
- `render.yaml` is included for Render auto-configuration

Example Docker deployment:
```bash
docker build -t brpap-app .
docker run -p 8000:8000 --env STRIPE_SECRET_KEY=sk_test_YOUR_SECRET_KEY --env DOMAIN_URL=http://localhost:8000 brpap-app
```

## Heroku deployment

This repo now includes a GitHub Actions workflow to deploy to Heroku on pushes to `main`.

1. Create a Heroku app.
2. Add these repository secrets:
   - `HEROKU_API_KEY`
   - `HEROKU_APP_NAME`
   - `HEROKU_EMAIL`
3. Push to `main` and the action will deploy automatically.

## Web experience

- The root page now serves an attractive landing page with live forecast preview
- Checkout flows redirect users to Stripe with `create-checkout-session`
- Success and cancel pages provide a polished subscription experience

## Notes

- Ensure a valid Stripe secret key is set before calling `/create-checkout-session`
- The Stripe route uses a subscription priced at $49.00 USD per month
