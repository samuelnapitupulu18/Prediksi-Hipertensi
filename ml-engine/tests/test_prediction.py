import os
import numpy as np
# pyrefly: ignore [missing-import]
import pytest
from app.models.xgboost_model import XGBoostModel

# Use mock model if available
MODEL_PATH = os.environ.get('MODEL_PATH', 'artifacts/xgboost_sgo_model.json')
METADATA_PATH = os.environ.get('METADATA_PATH', 'artifacts/model_metadata.json')

@pytest.fixture
def model():
    predictor = XGBoostModel()
    predictor.load(MODEL_PATH, METADATA_PATH)
    return predictor

def test_model_loads_successfully(model):
    assert model.model is not None
    assert model.version is not None

def test_prediction_returns_valid_risk_level(model):
    # Dummy scaled features
    X = np.array([[0.5] * 11])
    risk_level, confidence, probs = model.predict(X)
    
    assert risk_level in ['low', 'medium', 'high']
    assert len(probs) == 3
    assert 0 <= confidence <= 1.0

def test_probabilities_sum_to_one(model):
    X = np.array([[0.2] * 11])
    _, _, probs = model.predict(X)
    
    total = sum(probs.values())
    assert abs(total - 1.0) < 1e-5

def test_feature_importance_has_11_features(model):
    importance = model.get_feature_importances()
    assert len(importance) == 11
    assert "feature" in importance[0]
    assert "importance" in importance[0]
