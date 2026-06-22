import time
from fastapi import APIRouter, Depends, HTTPException, Request
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse, FeatureImportance
from app.pipeline.preprocessor import DataPreprocessor
from app.models.xgboost_model import XGBoostModel
from app.api.dependencies import get_model

router = APIRouter()

@router.get("/health", tags=["System"])
async def health_check(model: XGBoostModel = Depends(get_model)):
    """Health check endpoint. Verified model is loaded."""
    if not model.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_version": model.version}

@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict_risk(
    request: PredictionRequest,
    model: XGBoostModel = Depends(get_model)
):
    """Predicts hypertension risk based on patient clinical features."""
    start_time = time.time()
    
    if not model.is_loaded:
        raise HTTPException(status_code=503, detail="Model is not ready for inference")
        
    try:
        # 1. Preprocess data (Categorical encoding + Scaling)
        # Prevents data leakage by using static mappings/min-max from training
        x_processed = DataPreprocessor.process(request)
        
        # 2. Run inference
        risk_level, confidence, prob_dict = model.predict(x_processed)
        
        # 3. Get feature importance
        importances = model.get_feature_importances()
        fi_response = [FeatureImportance(**i) for i in importances]
        
        # Calculate execution time
        inference_time_ms = round((time.time() - start_time) * 1000, 2)
        
        # 4. Return formatted response
        return PredictionResponse(
            risk_level=risk_level,
            confidence_score=confidence,
            probability=prob_dict,
            feature_importance=fi_response,
            model_version=model.version,
            inference_time_ms=inference_time_ms
        )
        
    except ValueError as e:
        # Usually triggered by unknown categorical values
        raise HTTPException(status_code=422, detail=f"Preprocessing error: {str(e)}")
    except Exception as e:
        # Catch-all for unexpected inference errors
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
