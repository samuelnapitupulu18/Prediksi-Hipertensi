import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Hypertension Risk Early Detection - ML Engine"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Model configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", "artifacts/xgboost_sgo_model.json")
    MODEL_METADATA_PATH: str = os.getenv("MODEL_METADATA_PATH", "artifacts/model_metadata.json")

    class Config:
        case_sensitive = True

settings = Settings()
