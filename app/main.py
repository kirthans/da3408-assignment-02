from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

import joblib
from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_PATH = Path(__file__).resolve().parent.parent / "spam_model.joblib"
model = None

class PredictRequest(BaseModel):
    text: str = Field(min_length=1)

class PredictResponse(BaseModel):
    label: Literal["ham", "spam"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load(MODEL_PATH)
    print(f"Loaded model from {MODEL_PATH}")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    label = model.predict([request.text])[0]
    return {"label": label}