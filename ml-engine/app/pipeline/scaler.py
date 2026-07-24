from typing import Dict, Any

class StaticMinMaxScaler:
    """
    Applies Min-Max scaling using hardcoded min/max values derived from
    the training dataset to prevent data leakage during inference.
    """
    
    # Hardcoded ranges from training dataset
    FEATURE_RANGES = {
        "age": {"min": 18.0, "max": 100.0},
        "gender": {"min": 0.0, "max": 1.0},
        "bmi": {"min": 10.0, "max": 60.0},
        "smoking_status": {"min": 0.0, "max": 1.0},
        "physical_activity": {"min": 0.0, "max": 2.0},
        "family_history": {"min": 0.0, "max": 1.0},
        "red_meat_consumption": {"min": 0.0, "max": 2.0},
        "salt_consumption": {"min": 0.0, "max": 2.0},
        "systolic_bp": {"min": 70.0, "max": 250.0},
        "diastolic_bp": {"min": 40.0, "max": 150.0},
    }

    @classmethod
    def transform(cls, data: Dict[str, Any]) -> Dict[str, float]:
        scaled_data = {}
        for feature, val in data.items():
            if feature in cls.FEATURE_RANGES:
                f_min = cls.FEATURE_RANGES[feature]["min"]
                f_max = cls.FEATURE_RANGES[feature]["max"]
                
                # Avoid division by zero if min == max
                if f_max == f_min:
                    scaled_data[feature] = 0.0
                else:
                    # Clip values that might fall slightly outside training bounds
                    clipped_val = max(f_min, min(float(val), f_max))
                    scaled_data[feature] = (clipped_val - f_min) / (f_max - f_min)
            else:
                scaled_data[feature] = float(val)
                
        return scaled_data
