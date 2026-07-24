import time
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from app.schemas.request import PredictionRequest
from app.schemas.response import PredictionResponse, FeatureImportance
from app.pipeline.preprocessor import DataPreprocessor
from app.models.xgboost_model import XGBoostModel
from app.api.dependencies import get_model
from app.optimization.benchmark import run_comparison, run_timing_comparison

router = APIRouter()


class OptimizationRequest(BaseModel):
    """Parameter percobaan yang diatur manual oleh pengguna dari antarmuka."""

    # Batas atas hanya penjagaan agar permintaan tidak melampaui batas waktu HTTP.
    # SGO sendiri tidak punya batas iterasi; untuk percobaan yang lebih panjang,
    # gunakan skrip CLI scripts/run_sgo_experiment.py yang tidak dibatasi apa pun.
    iterations: int = Field(10, ge=1, le=500, description="Jumlah iterasi SGO")
    population_size: int = Field(6, ge=3, le=50, description="Ukuran populasi SGO")
    seed: int = Field(42, ge=0, le=9999, description="Seed acak agar hasil dapat diulang")
    verification_runs: int = Field(
        1, ge=1, le=10,
        description="Berapa kali optimasi diulang dengan seed berbeda untuk menguji konsistensi",
    )
    include_blood_pressure: bool = Field(
        False,
        description=(
            "Sertakan TDS & TDD sebagai fitur. Label dataset merupakan turunan "
            "pasti dari keduanya, sehingga mode ini membuat akurasi mencapai 100%."
        ),
    )

@router.get("/health", tags=["System"])
async def health_check(model: XGBoostModel = Depends(get_model)):
    """Health check endpoint. Verified model is loaded."""
    if not model.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_version": model.version}

@router.get("/model-info", tags=["System"])
async def model_info(model: XGBoostModel = Depends(get_model)):
    """
    Metadata model produksi yang sedang dimuat — apa adanya dari berkas artefak.

    Berisi angka hasil pengukuran saat pelatihan: metrik pada data uji,
    hyperparameter temuan SGO, dan kepentingan fitur yang dihitung dari model.
    Dipakai antarmuka agar tidak ada angka yang perlu ditulis di sisi frontend.
    """
    if not model.is_loaded:
        raise HTTPException(status_code=503, detail="Model belum dimuat")
    return model.metadata


class TimingRequest(BaseModel):
    """
    Parameter uji waktu eksekusi pada jumlah iterasi boosting yang ditentukan
    sendiri untuk masing-masing model.

    Catatan: `iterations` di sini berarti `n_estimators` — banyaknya putaran
    boosting (jumlah pohon) — BUKAN jumlah generasi pencarian SGO.
    """

    default_iterations: int = Field(100, ge=1, le=2000, description="Iterasi boosting model default")
    optimized_iterations: int = Field(100, ge=1, le=2000, description="Iterasi boosting model optimasi")
    seed: int = Field(42, ge=0, le=9999)
    repeats: int = Field(3, ge=1, le=10, description="Pengulangan pengukuran waktu, diambil mediannya")
    include_blood_pressure: bool = Field(False)


@router.post("/optimize/timing", tags=["Optimization"])
def compare_timing(request: TimingRequest):
    """
    Bandingkan akurasi dan waktu eksekusi model default vs model hasil optimasi
    pada jumlah iterasi boosting yang dapat ditentukan sendiri untuk masing-masing.

    Proses ini ringan (hanya melatih dua model), sehingga hasilnya muncul dalam
    hitungan detik dan cocok diperagakan langsung.
    """
    try:
        return run_timing_comparison(
            default_iterations=request.default_iterations,
            optimized_iterations=request.optimized_iterations,
            seed=request.seed,
            repeats=request.repeats,
            include_blood_pressure=request.include_blood_pressure,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menjalankan uji waktu: {e}")


@router.post("/optimize/compare", tags=["Optimization"])
def compare_optimization(request: OptimizationRequest):
    """
    Jalankan perbandingan sesungguhnya antara XGBoost Default dan XGBoost + SGO.

    Seluruh angka yang dikembalikan — akurasi, presisi, recall, F1, maupun waktu
    — dihasilkan dari pelatihan yang benar-benar dijalankan saat permintaan ini
    diproses. Tidak ada nilai yang ditetapkan sebelumnya.

    Endpoint ini didefinisikan sebagai fungsi biasa (bukan async) supaya FastAPI
    menjalankannya di threadpool, sehingga proses yang memakan waktu tidak
    memblokir endpoint lain seperti /health dan /predict.
    """
    try:
        return run_comparison(
            iterations=request.iterations,
            population_size=request.population_size,
            seed=request.seed,
            include_blood_pressure=request.include_blood_pressure,
            verification_runs=request.verification_runs,
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menjalankan optimasi: {e}")


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
