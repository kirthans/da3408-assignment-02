# Question 1 — Docker Image Comparison

| Image | Size |
|---|---:|
| Naive single-stage (`spam-api:naive`) | 2.1 GB |
| Multi-stage (`spam-api:multi`) | 841 MB |

Approximate reduction: `((2100 - 841) / 2100) × 100 = 60.0%`.

Both images successfully served `GET /healthz` and `POST /predict`.

The multi-stage image is smaller because its runtime stage uses `python:3.12-slim` rather than the naive image's full `python:3.12` base. The final stage copies only the API directory and `spam_model.joblib`; the dataset, dataset generator, training script, and the builder stage's temporary dependency-wheel directory are not retained in the final image.