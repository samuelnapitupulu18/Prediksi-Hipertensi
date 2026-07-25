import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.api.routes import router as api_router
from app.models.xgboost_model import XGBoostModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: muat model XGBoost ke memori satu kali saat server menyala,
    # sehingga setiap permintaan /predict tidak perlu membaca berkas model lagi.
    print(f"Loading XGBoost model from {settings.MODEL_PATH}...")
    model = XGBoostModel()

    # Server tetap menyala walau berkas model belum ada, hanya mencatat
    # peringatan — supaya model dapat dilatih lebih dulu tanpa crash.
    if os.path.exists(settings.MODEL_PATH):
        model.load(settings.MODEL_PATH, settings.MODEL_METADATA_PATH)
        print(f"Model loaded successfully. Version: {model.version}")
    else:
        print(f"WARNING: Model file not found at {settings.MODEL_PATH}.")
        print("Jalankan: python scripts/train_production_model.py untuk melatih model.")

    app.state.model = model

    yield

    # Logika shutdown (bila ada)
    print("Shutting down ML Engine...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    description="Hypertension Risk Prediction API utilizing SGO-Optimized XGBoost",
)

# Include routing
app.include_router(api_router)
