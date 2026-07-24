"""
Pelatihan Model Produksi — dari dataset hipertensi yang sesungguhnya
====================================================================

Skrip ini menggantikan `generate_mock_model.py`, yang sebelumnya melatih model
dari data acak `sklearn.make_classification` sehingga tidak ada kaitannya sama
sekali dengan hipertensi.

Yang dilakukan skrip ini:

1. Membaca dataset asli (`data/dataset_hipertensi.csv`).
2. Menerjemahkan kolom dataset menjadi nama fitur yang dipakai aplikasi.
3. Menjalankan data latih melalui **pipeline pra-pemrosesan yang sama persis**
   dengan yang dipakai saat inferensi (StaticLabelEncoder + StaticMinMaxScaler),
   sehingga tidak ada perbedaan perlakuan antara pelatihan dan penggunaan.
4. Mencari hyperparameter memakai Social Group Optimization yang sungguhan.
5. Melatih model akhir, mengukurnya pada data uji, lalu menyimpan model beserta
   metadata yang berisi **angka hasil pengukuran nyata** — termasuk kepentingan
   fitur yang dihitung dari model, bukan daftar yang ditulis tangan.

CATATAN PENTING MENGENAI KELAS
------------------------------
Dataset hanya memuat label biner (0 = tidak berisiko, 1 = berisiko), sedangkan
antarmuka menampilkan tiga tingkat risiko. Karena itu model dilatih sebagai
pengklasifikasi biner pada label ASLI dataset — tanpa mengarang label baru — dan
tiga tingkat risiko diturunkan dari ambang probabilitas keluaran model:

    peluang berisiko < 0.34            -> Rendah  (low)
    0.34 <= peluang berisiko <= 0.66   -> Sedang  (medium)
    peluang berisiko > 0.66            -> Tinggi  (high)

Dengan begitu tidak ada label buatan, dan penyajian tiga tingkat tetap dapat
dipertanggungjawabkan sebagai pembagian rentang keyakinan model.

CARA MENJALANKAN
----------------
    cd ml-engine
    .venv\\Scripts\\python.exe scripts/train_production_model.py
    .venv\\Scripts\\python.exe scripts/train_production_model.py --iterations 20 --population 8
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.pipeline.label_encoder import StaticLabelEncoder  # noqa: E402
from app.pipeline.preprocessor import DataPreprocessor  # noqa: E402
from app.pipeline.scaler import StaticMinMaxScaler  # noqa: E402
from app.optimization.sgo import SearchSpace, SocialGroupOptimizer  # noqa: E402

BASE_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = BASE_DIR / "data" / "dataset_hipertensi.csv"
MODEL_PATH = BASE_DIR / "artifacts" / "xgboost_sgo_model.json"
METADATA_PATH = BASE_DIR / "artifacts" / "model_metadata.json"

# Label Bahasa Indonesia untuk ditampilkan pada dashboard XAI
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

RISK_THRESHOLDS = {"low_max": 0.34, "high_min": 0.66}


def muat_dan_terjemahkan(path: Path) -> tuple[pd.DataFrame, np.ndarray]:
    """
    Baca dataset lalu terjemahkan kolomnya menjadi nama & format fitur yang
    dipakai aplikasi, persis seperti yang dikirim form skrining.
    """
    df = pd.read_csv(path)

    hasil = pd.DataFrame()
    hasil["age"] = df["Usia"].astype(int)
    hasil["gender"] = df["Jenis_Kelamin"].map({"Laki-laki": "male", "Perempuan": "female"})
    hasil["systolic_bp"] = df["TDS"].astype(int)
    hasil["diastolic_bp"] = df["TDD"].astype(int)
    hasil["bmi"] = df["IMT"].astype(float)
    hasil["family_history"] = df["Riwayat_Keluarga"].astype(bool)
    hasil["smoking_status"] = df["Merokok"].astype(bool)

    # Aktivitas fisik pada dataset sudah tiga tingkat (0/1/2) — cocok dengan form
    hasil["physical_activity"] = df["Aktivitas_Fisik"].map({0: "low", 1: "moderate", 2: "high"})

    # PENTING: konsumsi daging & garam pada dataset hanya DUA tingkat (0/1),
    # sedangkan form menyediakan tiga tingkat. Nilai 0 diperlakukan sebagai
    # "rendah" dan 1 sebagai "tinggi". Pemetaan ini didokumentasikan pada
    # metadata model agar perbedaannya tidak tersembunyi.
    hasil["red_meat_consumption"] = df["Konsumsi_Daging"].map({0: "low", 1: "high"})
    hasil["salt_consumption"] = df["Konsumsi_Garam"].map({0: "low", 1: "high"})

    y = df["Label"].astype(int).to_numpy()
    return hasil, y


def pra_proses(df: pd.DataFrame) -> np.ndarray:
    """
    Jalankan setiap baris melalui encoder & scaler YANG SAMA dengan inferensi.

    Memakai kelas yang sama persis (bukan menyalin logikanya) adalah jaminan
    bahwa tidak ada perbedaan perlakuan antara data latih dan data yang masuk
    dari form skrining.
    """
    urutan = DataPreprocessor.get_feature_names()
    baris: List[List[float]] = []

    for catatan in df.to_dict(orient="records"):
        ter_encode = StaticLabelEncoder.transform(catatan)
        ter_skala = StaticMinMaxScaler.transform(ter_encode)
        baris.append([ter_skala[f] for f in urutan])

    return np.asarray(baris, dtype=float)


def bangun_model(params: Dict[str, Any], seed: int) -> xgb.XGBClassifier:
    return xgb.XGBClassifier(
        learning_rate=float(params["learning_rate"]),
        max_depth=int(params["max_depth"]),
        n_estimators=int(params["n_estimators"]),
        objective="binary:logistic",
        eval_metric="logloss",
        tree_method="hist",
        n_jobs=-1,
        random_state=seed,
        verbosity=0,
    )


def main() -> int:
    p = argparse.ArgumentParser(description="Latih model produksi dari dataset asli")
    p.add_argument("--iterations", type=int, default=15, help="Iterasi SGO")
    p.add_argument("--population", type=int, default=6, help="Ukuran populasi SGO")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    garis = "=" * 76
    print(garis)
    print(" PELATIHAN MODEL PRODUKSI — dataset hipertensi asli")
    print(garis)

    if not DATASET_PATH.exists():
        print(f"Dataset tidak ditemukan: {DATASET_PATH}", file=sys.stderr)
        return 1

    df, y = muat_dan_terjemahkan(DATASET_PATH)
    X = pra_proses(df)
    urutan_fitur = DataPreprocessor.get_feature_names()

    print(f" Dataset      : {DATASET_PATH.name}")
    print(f" Jumlah sampel: {len(y):,}".replace(",", "."))
    print(f" Fitur ({len(urutan_fitur)})  : {', '.join(urutan_fitur)}")
    print(f" Distribusi   : tidak berisiko={int((y == 0).sum())}, berisiko={int((y == 1).sum())}")
    print(garis)

    X_train, X_tmp, y_train, y_tmp = train_test_split(
        X, y, test_size=0.4, random_state=args.seed, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_tmp, y_tmp, test_size=0.5, random_state=args.seed, stratify=y_tmp
    )
    print(f" Pembagian    : {len(y_train)} latih / {len(y_val)} validasi / {len(y_test)} uji")
    print()

    # ------------------------------------------------------------ optimasi SGO
    print(f" Menjalankan SGO ({args.iterations} iterasi, populasi {args.population})...")

    def fitness(params: Dict[str, float]) -> float:
        model = bangun_model(params, args.seed)
        model.fit(X_train, y_train)
        return float(f1_score(y_val, model.predict(X_val), average="macro", zero_division=0))

    ruang = [
        SearchSpace("learning_rate", 0.01, 0.30),
        SearchSpace("max_depth", 3, 12, is_integer=True),
        SearchSpace("n_estimators", 50, 300, is_integer=True),
    ]

    def lapor(rec):
        if not args.quiet:
            print(f"   iterasi {rec.iteration:>3}/{args.iterations}  fitness {rec.best_fitness * 100:.3f}%")

    mulai = time.perf_counter()
    hasil_sgo = SocialGroupOptimizer(
        space=ruang,
        fitness_fn=fitness,
        population_size=args.population,
        iterations=args.iterations,
        seed=args.seed,
    ).optimize(on_iteration=lapor)
    lama_optimasi = time.perf_counter() - mulai

    best = {
        "learning_rate": round(float(hasil_sgo.best_params["learning_rate"]), 4),
        "max_depth": int(hasil_sgo.best_params["max_depth"]),
        "n_estimators": int(hasil_sgo.best_params["n_estimators"]),
    }
    print(f" Selesai dalam {lama_optimasi:.1f} detik, {hasil_sgo.n_evaluations} pelatihan model.")
    print(f" Hyperparameter terbaik: {best}")
    print()

    # ------------------------------------------------------- model akhir + uji
    model = bangun_model(best, args.seed)
    mulai = time.perf_counter()
    model.fit(X_train, y_train)
    lama_latih = time.perf_counter() - mulai

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrik = {
        "accuracy": round(float(accuracy_score(y_test, y_pred)) * 100, 2),
        "precision_macro": round(float(precision_score(y_test, y_pred, average="macro", zero_division=0)) * 100, 2),
        "recall_macro": round(float(recall_score(y_test, y_pred, average="macro", zero_division=0)) * 100, 2),
        "f1_macro": round(float(f1_score(y_test, y_pred, average="macro", zero_division=0)) * 100, 2),
        "auc": round(float(roc_auc_score(y_test, y_proba)) * 100, 2),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=[0, 1]).tolist(),
    }

    print(garis)
    print(" HASIL PENGUKURAN PADA DATA UJI")
    print("-" * 76)
    for k in ("accuracy", "precision_macro", "recall_macro", "f1_macro", "auc"):
        print(f"   {k:<18}: {metrik[k]}%")
    print(f"   confusion_matrix  : {metrik['confusion_matrix']}")
    print()

    # ------------------------------------------- kepentingan fitur SESUNGGUHNYA
    # Dihitung dari model dengan metode 'gain', bukan daftar yang ditulis tangan.
    skor = model.get_booster().get_score(importance_type="gain")
    mentah = {}
    for i, nama in enumerate(urutan_fitur):
        mentah[nama] = float(skor.get(f"f{i}", 0.0))

    total = sum(mentah.values()) or 1.0
    kepentingan = [
        {
            "feature": nama,
            "importance": round(nilai / total, 4),
            "label": FEATURE_LABELS.get(nama, nama),
        }
        for nama, nilai in sorted(mentah.items(), key=lambda kv: kv[1], reverse=True)
    ]

    print(" KEPENTINGAN FITUR (gain, dinormalisasi) — dihitung dari model")
    print("-" * 76)
    for item in kepentingan:
        bar = "#" * int(item["importance"] * 50)
        print(f"   {item['label']:<32} {item['importance']:.4f}  {bar}")
    print()

    # sebaran probabilitas -> memastikan pembagian tiga tingkat masuk akal
    rendah = int((y_proba < RISK_THRESHOLDS["low_max"]).sum())
    tinggi = int((y_proba > RISK_THRESHOLDS["high_min"]).sum())
    sedang = len(y_proba) - rendah - tinggi
    print(" SEBARAN TINGKAT RISIKO pada data uji (dari ambang probabilitas)")
    print("-" * 76)
    print(f"   Rendah (<{RISK_THRESHOLDS['low_max']})   : {rendah}")
    print(f"   Sedang            : {sedang}")
    print(f"   Tinggi (>{RISK_THRESHOLDS['high_min']})  : {tinggi}")
    print()

    # ------------------------------------------------------------- simpan hasil
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    model.save_model(str(MODEL_PATH))

    metadata = {
        "version": "2.0.0-sgo",
        "algorithm": "XGBoost",
        "optimization": "Social Group Optimization (SGO)",
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset": {
            "file": DATASET_PATH.name,
            "total_samples": int(len(y)),
            "split": {"train": int(len(y_train)), "validation": int(len(y_val)), "test": int(len(y_test))},
            "class_distribution": {
                "tidak_berisiko": int((y == 0).sum()),
                "berisiko": int((y == 1).sum()),
            },
        },
        "task": "binary classification (0 = tidak berisiko, 1 = berisiko)",
        "risk_level_thresholds": RISK_THRESHOLDS,
        "feature_order": urutan_fitur,
        "hyperparameters": best,
        "hyperparameter_search": {
            "method": "Social Group Optimization",
            "iterations": args.iterations,
            "population_size": args.population,
            "seed": args.seed,
            "fitness": "macro F1 pada data validasi",
            "best_validation_fitness": round(hasil_sgo.best_fitness * 100, 2),
            "model_trainings": hasil_sgo.n_evaluations,
            "optimization_seconds": round(lama_optimasi, 2),
        },
        "metrics_test_set": metrik,
        "training_seconds": round(lama_latih, 3),
        "feature_importance": kepentingan,
        "notes": [
            "Model dilatih dari dataset hipertensi asli, bukan data sintetis acak.",
            "Pra-pemrosesan memakai StaticLabelEncoder dan StaticMinMaxScaler yang "
            "sama persis dengan yang dipakai saat inferensi.",
            "Label dataset hanya dua kelas; tiga tingkat risiko pada antarmuka "
            "diturunkan dari ambang probabilitas, bukan dari label buatan.",
            "Dataset hanya membedakan konsumsi daging dan garam menjadi dua tingkat "
            "(0 = rendah, 1 = tinggi), sedangkan form menyediakan tiga tingkat.",
            "Kepentingan fitur dihitung dari model dengan metode gain.",
        ],
    }

    METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    print(garis)
    print(f" Model    disimpan ke : {MODEL_PATH}")
    print(f" Metadata disimpan ke : {METADATA_PATH}")
    print(garis)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
