from pydantic import BaseModel
from typing import Dict, List, Literal

class FeatureImportance(BaseModel):
    feature: str
    importance: float
    # Label siap-tampil (Bahasa Indonesia) untuk dashboard XAI
    label: str

class PredictionResponse(BaseModel):
    risk_level: Literal["low", "medium", "high"]
    confidence_score: float
    probability: Dict[str, float]
    feature_importance: List[FeatureImportance]
    model_version: str
    inference_time_ms: float
