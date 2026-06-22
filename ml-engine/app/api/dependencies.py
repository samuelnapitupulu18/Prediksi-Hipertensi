from fastapi import Request
from app.models.xgboost_model import XGBoostModel

def get_model(request: Request) -> XGBoostModel:
    """Dependency to get the loaded XGBoost model from app state."""
    return request.app.state.model
