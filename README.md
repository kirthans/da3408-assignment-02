# AIOps Module 3 Assignment — Spam Detection API

A REST API that classifies short messages as `spam` or `ham` using a TF-IDF vectorizer and Multinomial Naive Bayes model.

## API contract

- `POST /predict` accepts `{"text": "..."}` and returns `{"label": "spam"}` or `{"label": "ham"}`.
- `GET /healthz` returns HTTP 200 after the model loads.

## Local setup

```bash
conda env create -f environment.yml
conda activate aioops-spam
python generate_dataset.py
python train.py
uvicorn app.main:app --host 0.0.0.0 --port 8000