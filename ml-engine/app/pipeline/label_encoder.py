from typing import Dict, Any

class StaticLabelEncoder:
    """
    Statically encodes categorical variables to numeric values based on 
    hardcoded mappings to prevent data leakage.
    """
    
    # These mappings must exactly match the training data transformations
    MAPPINGS = {
        "gender": {
            "male": 0,
            "female": 1
        },
        "smoking_status": {
            "never": 0,
            "former": 1,
            "current": 2
        },
        "alcohol_consumption": {
            "none": 0,
            "moderate": 1,
            "heavy": 2
        },
        "physical_activity": {
            "low": 0,
            "moderate": 1,
            "high": 2
        },
        "cholesterol_level": {
            "normal": 0,
            "borderline": 1,
            "high": 2
        }
    }

    @classmethod
    def transform(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        encoded_data = data.copy()
        for feature, mapping in cls.MAPPINGS.items():
            if feature in encoded_data:
                # Convert string to lowercase for safe matching
                val = str(encoded_data[feature]).lower()
                if val in mapping:
                    encoded_data[feature] = mapping[val]
                else:
                    raise ValueError(f"Unknown category '{val}' for feature '{feature}'")
        
        # Handle boolean features
        if "family_history" in encoded_data:
            encoded_data["family_history"] = 1 if encoded_data["family_history"] else 0
            
        if "diabetes" in encoded_data:
            encoded_data["diabetes"] = 1 if encoded_data["diabetes"] else 0
            
        return encoded_data
