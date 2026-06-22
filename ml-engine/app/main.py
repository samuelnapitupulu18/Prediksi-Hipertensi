import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.api.routes import router as api_router
from app.models.xgboost_model import XGBoostModel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load the XGBoost model into memory
    print(f"Loading XGBoost model from {settings.MODEL_PATH}...")
    model = XGBoostModel()
    
    # We don't crash if the file isn't there yet, just log an error
    # so we can run generate_mock_model.py later.
    if os.path.exists(settings.MODEL_PATH):
        model.load(settings.MODEL_PATH, settings.MODEL_METADATA_PATH)
        print(f"Model loaded successfully. Version: {model.version}")
    else:
        print(f"WARNING: Model file not found at {settings.MODEL_PATH}.")
        print("Please run scripts/generate_mock_model.py to create a dummy model.")
        
    app.state.model = model
    
    yield
    
    # Shutdown logic (if any)
    print("Shutting down ML Engine...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
    description="Hypertension Risk Prediction API utilizing SGO-Optimized XGBoost",
)

# Include routing
app.include_router(api_router)
