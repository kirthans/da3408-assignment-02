import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

import joblib
import redis
from fastapi import FastAPI
from pydantic import BaseModel, Field
from redis.exceptions import RedisError

MODEL_PATH = Path(__file__).resolve().parent.parent / "spam_model.joblib"
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
APP_VERSION = os.getenv("APP_VERSION", "v2")
CACHE_TTL_SECONDS = 3600

model = None
redis_client = None

class PredictRequest(BaseModel):
    text: str = Field(min_length=1)

class PredictResponse(BaseModel):
    label: Literal["ham", "spam"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, redis_client
    model = joblib.load(MODEL_PATH)
    redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    print(f"Loaded model from {MODEL_PATH}")
    print(f"Configured Redis client for {REDIS_URL}")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": APP_VERSION}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    cache_key = f"spam-prediction:{request.text}"

    try:
        cached_label = redis_client.get(cache_key)
        if cached_label is not None:
            print("Cache HIT")
            return {"label": cached_label}
    except RedisError:
        print("Redis unavailable; serving uncached prediction")
    
    label = str(model.predict([request.text])[0])

    try:
        redis_client.setex(cache_key, CACHE_TTL_SECONDS, label)
        print("Cache MISS; prediction is now stored in Redis")
    except RedisError:
        print("Redis unavailable; label not cached")

    return {"label": label}