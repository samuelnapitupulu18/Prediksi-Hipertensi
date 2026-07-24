import numpy as np
from typing import Dict, Any, List
from app.schemas.request import PredictionRequest
from app.pipeline.label_encoder import StaticLabelEncoder
from app.pipeline.scaler import StaticMinMaxScaler

class DataPreprocessor:
    """
    Orchestrates the data transformation pipeline.
    """
    
    # Feature order must strictly match model training order
    FEATURE_ORDER = [
        "age",
        "gender",
        "systolic_bp",
        "diastolic_bp",
        "bmi",
        "family_history",
        "physical_activity",
        "smoking_status",
        "red_meat_consumption",
        "salt_consumption"
    ]

    @classmethod
    def process(cls, request: PredictionRequest) -> np.ndarray:
        # 1. Convert to dict
        data_dict = request.model_dump()
        
        # 2. Label Encoding (Categorical -> Numeric)
        encoded_data = StaticLabelEncoder.transform(data_dict)
        
        # 3. Min-Max Scaling (Numeric -> [0, 1])
        scaled_data = StaticMinMaxScaler.transform(encoded_data)
        
        # 4. Order features into an array
        ordered_features = [scaled_data[feature] for feature in cls.FEATURE_ORDER]
        
        # 5. Return as 2D numpy array for XGBoost: shape (1, n_features)
        return np.array([ordered_features])

    @classmethod
    def get_feature_names(cls) -> List[str]:
        return cls.FEATURE_ORDER
