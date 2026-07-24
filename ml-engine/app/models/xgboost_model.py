import os
import json
import xgboost as xgb
import numpy as np
from typing import Dict, List, Any, Tuple
from app.pipeline.preprocessor import DataPreprocessor


class XGBoostModel:
    """
    Pembungkus model XGBoost untuk inferensi.

    CATATAN MENGENAI KELAS
    ----------------------
    Model dilatih sebagai pengklasifikasi BINER pada label asli dataset
    (0 = tidak berisiko, 1 = berisiko), karena dataset memang hanya memuat dua
    kelas. Tidak ada label buatan.

    Antarmuka menampilkan tiga tingkat risiko. Ketiganya diturunkan dari peluang
    keluaran model memakai ambang yang tersimpan pada metadata:

        peluang berisiko < low_max        -> low
        low_max <= peluang <= high_min    -> medium
        peluang > high_min                -> high

    Model tiga kelas versi lama tetap ditangani agar berkas artefak lama masih
    dapat dimuat tanpa mengubah kode.
    """

    DEFAULT_THRESHOLDS = {"low_max": 0.34, "high_min": 0.66}

    # Dipakai hanya bila metadata tidak menyertakan label.
    FEATURE_LABELS = {
        "age": "Usia",
        "gender": "Jenis Kelamin",
        "systolic_bp": "Tekanan Darah Sistolik (TDS)",
        "diastolic_bp": "Tekanan Darah Diastolik (TDD)",
        "bmi": "Indeks Massa Tubuh (IMT)",
        "family_history": "Riwayat Keluarga",
        "physical_activity": "Aktivitas Fisik",
        "smoking_status": "Status Perokok",
        "red_meat_consumption": "Konsumsi Daging Merah",
        "salt_consumption": "Konsumsi Garam",
    }

    def __init__(self):
        self.model = None
        self.metadata: Dict[str, Any] = {}
        self.feature_names = DataPreprocessor.get_feature_names()
        self.is_loaded = False
        self.version = "unknown"
        self.thresholds = dict(self.DEFAULT_THRESHOLDS)

    def load(self, model_path: str, metadata_path: str):
        """Memuat model XGBoost beserta metadatanya."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")

        self.model = xgb.XGBClassifier()
        self.model.load_model(model_path)

        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
                self.version = self.metadata.get("version", "unknown")
                ambang = self.metadata.get("risk_level_thresholds")
                if isinstance(ambang, dict):
                    self.thresholds.update(ambang)

        self.is_loaded = True

    # ------------------------------------------------------------------ utils
    def _tingkat_dari_peluang(self, peluang_berisiko: float) -> Tuple[str, Dict[str, float]]:
        """
        Ubah peluang biner menjadi tiga tingkat risiko beserta sebarannya.

        Bobot kelas 'medium' memuncak di wilayah tengah lalu meluruh ke arah
        kedua ujung, sehingga sebaran yang ditampilkan tetap informatif tanpa
        mengarang angka.
        """
        p = float(np.clip(peluang_berisiko, 0.0, 1.0))
        low_max = float(self.thresholds["low_max"])
        high_min = float(self.thresholds["high_min"])

        if p < low_max:
            tingkat = "low"
        elif p > high_min:
            tingkat = "high"
        else:
            tingkat = "medium"

        tengah = (low_max + high_min) / 2.0
        lebar = max(high_min - low_max, 1e-6)
        kedekatan = max(0.0, 1.0 - abs(p - tengah) / lebar)

        bobot_medium = kedekatan
        sisa = max(1.0 - bobot_medium, 0.0)
        bobot_high = sisa * p
        bobot_low = sisa * (1.0 - p)

        total = bobot_low + bobot_medium + bobot_high or 1.0
        sebaran = {
            "low": round(bobot_low / total, 6),
            "medium": round(bobot_medium / total, 6),
            "high": round(bobot_high / total, 6),
        }
        return tingkat, sebaran

    # ---------------------------------------------------------------- predict
    def predict(self, x: np.ndarray) -> Tuple[str, float, Dict[str, float]]:
        """Menjalankan inferensi; mengembalikan tingkat risiko, keyakinan, sebaran."""
        if not self.is_loaded:
            raise RuntimeError("Model is not loaded. Call load() first.")

        probas = self.model.predict_proba(x)[0]

        # Model tiga kelas (artefak versi lama)
        if len(probas) == 3:
            kelas = ["low", "medium", "high"]
            sebaran = {kelas[i]: float(probas[i]) for i in range(3)}
            idx = int(np.argmax(probas))
            return kelas[idx], float(probas[idx]), sebaran

        # Model biner (versi sekarang)
        peluang_berisiko = float(probas[1])
        tingkat, sebaran = self._tingkat_dari_peluang(peluang_berisiko)
        return tingkat, sebaran[tingkat], sebaran

    # ------------------------------------------------------- feature importance
    def get_feature_importances(self) -> List[Dict[str, Any]]:
        """
        Kepentingan fitur yang SESUNGGUHNYA dari model.

        Urutan pengambilan:
          1. Daftar pada metadata — dihitung saat pelatihan dengan metode gain.
          2. Bila tidak ada, dihitung langsung dari booster yang sedang dimuat.

        Tidak ada satu pun nilai yang ditulis tangan di berkas ini.
        """
        if not self.is_loaded:
            return []

        tersimpan = self.metadata.get("feature_importance")
        if isinstance(tersimpan, list) and tersimpan:
            return tersimpan

        try:
            skor = self.model.get_booster().get_score(importance_type="gain")
        except Exception:
            return []

        mentah = {
            nama: float(skor.get(f"f{i}", 0.0))
            for i, nama in enumerate(self.feature_names)
        }
        total = sum(mentah.values()) or 1.0

        return [
            {
                "feature": nama,
                "importance": round(nilai / total, 4),
                "label": self.FEATURE_LABELS.get(nama, nama),
            }
            for nama, nilai in sorted(mentah.items(), key=lambda kv: kv[1], reverse=True)
        ]
