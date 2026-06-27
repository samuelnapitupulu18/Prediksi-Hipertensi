import os
import pytest
from app.models.xgboost_model import XGBoostPredictor

# Use mock model if available
MODEL_PATH = os.environ.get('MODEL_PATH', 'artifacts/xgboost_sgo_model.json')

@pytest.fixture
def model():
    predictor = XGBoostPredictor(MODEL_PATH)
    predictor.load()
    return predictor

def test_model_loads_successfully(model):
    assert model.model is not None
    assert model.version is not None

def test_prediction_returns_valid_risk_level(model):
    # Dummy scaled features
    X = [[0.5] * 11]
    risk_level, probs = model.predict(X)
    
    assert risk_level in ['low', 'medium', 'high']
    assert len(probs) == 3

def test_probabilities_sum_to_one(model):
    X = [[0.2] * 11]
    _, probs = model.predict(X)
    
    total = sum(probs.values())
    assert abs(total - 1.0) < 1e-5

def test_feature_importance_has_11_features(model):
    importance = model.get_feature_importance()
    assert len(importance) == 11
    assert "feature" in importance[0]
    assert "importance" in importance[0]
