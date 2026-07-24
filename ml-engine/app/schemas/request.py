from pydantic import BaseModel, Field
from typing import Literal

class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Umur pasien dalam tahun")
    gender: Literal["male", "female"] = Field(..., description="Jenis kelamin pasien")
    bmi: float = Field(..., ge=10.0, le=60.0, description="Body Mass Index")
    family_history: bool = Field(..., description="Riwayat keluarga hipertensi")
    physical_activity: Literal["low", "moderate", "high"] = Field(..., description="Aktivitas fisik")
    smoking_status: bool = Field(..., description="Status perokok aktif/pasif")
    red_meat_consumption: Literal["low", "moderate", "high"] = Field(..., description="Konsumsi daging merah")
    salt_consumption: Literal["low", "moderate", "high"] = Field(..., description="Konsumsi garam berlebih")
    systolic_bp: int = Field(..., ge=70, le=250, description="Tekanan darah sistolik")
    diastolic_bp: int = Field(..., ge=40, le=150, description="Tekanan darah diastolik")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 45,
                "gender": "male",
                "bmi": 28.5,
                "family_history": True,
                "physical_activity": "low",
                "smoking_status": False,
                "red_meat_consumption": "moderate",
                "salt_consumption": "moderate",
                "systolic_bp": 135,
                "diastolic_bp": 88
            }
        }
