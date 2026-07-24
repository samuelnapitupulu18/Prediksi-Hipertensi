import os
import json
import xgboost as xgb
from sklearn.datasets import make_classification

def generate_mock_model():
    """
    Generates a dummy XGBoost model and saves it as a JSON file 
    so the ML Engine API can be tested end-to-end.
    """
    print("Generating Mock XGBoost Model...")
    
    # Create artifacts directory if not exists
    os.makedirs('artifacts', exist_ok=True)
    
    # We have 10 features defined in DataPreprocessor
    n_features = 10
    
    # Generate some random synthetic data for training the dummy model
    # We need 3 classes (low, medium, high)
    X, y = make_classification(
        n_samples=1000, 
        n_features=n_features, 
        n_informative=5, 
        n_classes=3, 
        random_state=42
    )
    
    # SGO Optimized params according to our doc:
    # learning_rate: 0.035, max_depth: 9, n_estimators: 285
    model = xgb.XGBClassifier(
        learning_rate=0.035,
        max_depth=9,
        n_estimators=100, # Using 100 here to make generation faster
        objective='multi:softprob',
        num_class=3
    )
    
    print("Training dummy model on synthetic data...")
    model.fit(X, y)
    
    # Save the model
    model_path = 'artifacts/xgboost_sgo_model.json'
    model.save_model(model_path)
    print(f"Model saved to {model_path}")
    
    # Save metadata
    metadata = {
        "version": "1.0.0-sgo-mock",
        "algorithm": "XGBoost",
        "optimization": "Social Group Optimization (SGO) - MOCK",
        "hyperparameters": {
            "learning_rate": 0.035,
            "max_depth": 9,
            "n_estimators": 285
        },
        "description": "This is a synthetic dummy model generated for testing the API."
    }
    
    meta_path = 'artifacts/model_metadata.json'
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    print(f"Metadata saved to {meta_path}")

if __name__ == "__main__":
    generate_mock_model()
