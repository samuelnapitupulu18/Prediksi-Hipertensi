import os
import json
import xgboost as xgb
import numpy as np
from typing import Dict, List, Any, Tuple
from app.pipeline.preprocessor import DataPreprocessor

class XGBoostModel:
    def __init__(self):
        self.model = None
        self.metadata = {}
        self.feature_names = DataPreprocessor.get_feature_names()
        self.is_loaded = False
        self.version = "unknown"

    def load(self, model_path: str, metadata_path: str):
        """Loads the XGBoost model and its metadata."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        # Load XGBoost model
        self.model = xgb.XGBClassifier()
        self.model.load_model(model_path)
        
        # Load metadata if exists
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
                self.version = self.metadata.get("version", "1.0.0-sgo")
                
        self.is_loaded = True

    def predict(self, x: np.ndarray) -> Tuple[str, float, Dict[str, float]]:
        """
        Runs inference and returns risk level, confidence, and prob distributions.
        """
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded. Call load() first.")
            
        # Get probabilities
        probas = self.model.predict_proba(x)[0]
        
        # In our model: 0 = low, 1 = medium, 2 = high
        classes = ["low", "medium", "high"]
        
        # Map probabilities to classes
        prob_dict = {classes[i]: float(probas[i]) for i in range(len(classes))}
        
        # Get predicted class (highest prob)
        pred_idx = int(np.argmax(probas))
        risk_level = classes[pred_idx]
        confidence = float(probas[pred_idx])
        
        return risk_level, confidence, prob_dict

    def get_feature_importances(self) -> List[Dict[str, Any]]:
        """Returns feature importances mapped to feature names, sorted."""
        if not self.is_loaded:
            return []
            
        # Get importances
        importances = self.model.feature_importances_
        
        # Map to feature names
        fi_list = []
        for i, name in enumerate(self.feature_names):
            fi_list.append({
                "feature": name,
                "importance": float(importances[i])
            })
            
        # Sort by importance descending
        fi_list.sort(key=lambda x: x["importance"], reverse=True)
        return fi_list
