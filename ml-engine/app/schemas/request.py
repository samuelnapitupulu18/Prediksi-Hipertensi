from pydantic import BaseModel, Field
from typing import Literal

class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Umur pasien dalam tahun")
    gender: Literal["male", "female"] = Field(..., description="Jenis kelamin pasien")
    bmi: float = Field(..., ge=10.0, le=60.0, description="Body Mass Index")
    smoking_status: Literal["never", "former", "current"] = Field(..., description="Status merokok")
    alcohol_consumption: Literal["none", "moderate", "heavy"] = Field(..., description="Konsumsi alkohol")
    physical_activity: Literal["low", "moderate", "high"] = Field(..., description="Aktivitas fisik")
    family_history: bool = Field(..., description="Riwayat keluarga hipertensi")
    diabetes: bool = Field(..., description="Penderita diabetes")
    systolic_bp: int = Field(..., ge=70, le=250, description="Tekanan darah sistolik")
    diastolic_bp: int = Field(..., ge=40, le=150, description="Tekanan darah diastolik")
    cholesterol_level: Literal["normal", "borderline", "high"] = Field(..., description="Kadar kolesterol")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "gender": "male",
                "bmi": 28.5,
                "smoking_status": "former",
                "alcohol_consumption": "moderate",
                "physical_activity": "low",
                "family_history": True,
                "diabetes": False,
                "systolic_bp": 135,
                "diastolic_bp": 88,
                "cholesterol_level": "high"
            }
        }
