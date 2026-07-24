from typing import Dict, Any

class StaticLabelEncoder:
    """
    Statically encodes categorical variables to numeric values based on 
    hardcoded mappings to prevent data leakage.
    """
    
    # These mappings must exactly match the training data transformations
    MAPPINGS = {
        "gender": {
            "female": 0,
            "male": 1
        },
        "physical_activity": {
            "low": 0,
            "moderate": 1,
            "high": 2
        },
        "red_meat_consumption": {
            "low": 0,
            "moderate": 1,
            "high": 2
        },
        "salt_consumption": {
            "low": 0,
            "moderate": 1,
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
        for bool_feature in ["family_history", "smoking_status"]:
            if bool_feature in encoded_data:
                encoded_data[bool_feature] = 1 if encoded_data[bool_feature] else 0
            
        return encoded_data
