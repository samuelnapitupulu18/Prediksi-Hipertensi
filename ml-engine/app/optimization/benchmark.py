"""
Pembanding XGBoost Default vs XGBoost + SGO
===========================================

Modul ini menjalankan eksperimen yang SESUNGGUHNYA:

* Melatih XGBoost dengan hyperparameter bawaan pustaka (tanpa penyetelan).
* Menjalankan Social Group Optimization untuk mencari hyperparameter terbaik,
  dengan jumlah iterasi dan ukuran populasi yang ditentukan pengguna.
* Melatih ulang XGBoost memakai hyperparameter temuan SGO.
* Mengukur metrik (accuracy, precision, recall, F1) pada data uji yang sama
  serta mencatat waktu nyata: lama optimasi, lama pelatihan, dan lama inferensi.

Tidak ada angka yang ditetapkan di muka. Seluruh nilai yang dilaporkan berasal
dari hasil pelatihan dan pengukuran saat itu juga.

TARGET KLASIFIKASI
------------------
Memakai kolom `Label` asli pada dataset — 2 kelas:
    0 = Tidak Berisiko Hipertensi
    1 = Berisiko Hipertensi
Label tidak diturunkan dari fitur mana pun, sehingga tidak terjadi kebocoran
informasi (data leakage) dan selisih performa antar model menjadi bermakna.

PEMBAGIAN DATA
--------------
    60% latih | 20% validasi | 20% uji

SGO hanya boleh "melihat" data validasi ketika mencari hyperparameter. Metrik
akhir yang dilaporkan dihitung pada data uji yang belum pernah disentuh selama
proses optimasi.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

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

from app.optimization.sgo import IterationRecord, SearchSpace, SocialGroupOptimizer

# Lokasi dataset di dalam project (disalin agar eksperimen dapat direproduksi)
DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "dataset_hipertensi.csv"

TARGET_COLUMN = "Label"
DROP_COLUMNS = ["Label", "Sumber"]

# Kolom tekanan darah — dipisahkan karena menentukan sifat eksperimen.
BLOOD_PRESSURE_COLUMNS = ["TDS", "TDD"]

CLASS_NAMES = ["Tidak Berisiko", "Berisiko"]

# CATATAN PENTING MENGENAI DATASET
# --------------------------------
# Pada dataset ini kolom `Label` ternyata merupakan rumus pasti dari tekanan
# darah: Label = 0 bila (TDS < 120 DAN TDD < 80), selain itu Label = 1.
# Kecocokan aturan tersebut 100% pada seluruh 10.000 baris, baik bagian Kaggle
# maupun Puskesmas.
#
# Konsekuensinya:
#   * MODE "dengan tensi"  -> TDS & TDD ikut menjadi fitur. Model apa pun akan
#     mencapai akurasi 100% karena tinggal menghafal aturannya. Perbandingan
#     Default vs SGO hanya bermakna pada sisi WAKTU, bukan akurasi.
#   * MODE "tanpa tensi"   -> TDS & TDD dikeluarkan. Model harus memprediksi
#     risiko dari faktor gaya hidup & demografi saja. Ini persoalan pembelajaran
#     yang sesungguhnya, sehingga selisih akurasi Default vs SGO menjadi nyata.
#     Mode ini juga sejalan dengan tujuan deteksi DINI: menapis risiko sebelum
#     pasien sempat diukur tensinya.
FEATURE_SET_DESCRIPTION = {
    True: (
        "Seluruh fitur termasuk tekanan darah (TDS & TDD). Label pada dataset "
        "merupakan turunan pasti dari TDS/TDD, sehingga akurasi kedua model "
        "akan mencapai 100% dan perbandingan hanya bermakna pada sisi waktu."
    ),
    False: (
        "Tanpa tekanan darah (TDS & TDD dikeluarkan). Model memprediksi risiko "
        "dari faktor gaya hidup dan demografi saja — sesuai tujuan deteksi dini "
        "sebelum pengukuran tensi. Inilah mode dengan persoalan pembelajaran nyata."
    ),
}

# --------------------------------------------------------------------------
# TIGA PARAMETER YANG DIUJI
# --------------------------------------------------------------------------
# Eksperimen ini sengaja dibatasi pada tiga hyperparameter yang selama ini
# dipaparkan pada laporan, supaya pembuktiannya lurus dan mudah diperiksa:
# apakah SGO benar-benar menghasilkan nilai tersebut, atau tidak.
TUNED_PARAMETERS = ["learning_rate", "max_depth", "n_estimators"]

# Ruang pencarian yang dijelajahi SGO untuk ketiga parameter tersebut.
SEARCH_SPACE = [
    SearchSpace("learning_rate", 0.01, 0.30),
    SearchSpace("max_depth", 3, 12, is_integer=True),
    SearchSpace("n_estimators", 50, 300, is_integer=True),
]

# Nilai bawaan pustaka XGBoost — inilah yang dilaporkan sebagai kolom "Default".
#
# CATATAN: nilai ini TIDAK diketik manual. Fungsi _library_default_params() di
# bawah membacanya langsung dari pustaka XGBoost yang terpasang, sehingga bila
# ditanya "dari mana angka 0.3 / 6 / 100?", jawabannya dapat ditunjukkan pada
# saat itu juga — bukan sekadar mengutip dokumentasi.
#
# Sejak XGBoost 2.x, XGBClassifier().get_params() mengembalikan None untuk
# ketiga parameter tersebut karena penetapan nilainya diserahkan ke inti C++.
# Karena itu nilainya diambil dari konfigurasi booster setelah pelatihan.
_DEFAULT_PARAMS_CACHE: Dict[str, Any] | None = None


def _library_default_params() -> Dict[str, Any]:
    """Baca nilai bawaan XGBoost langsung dari pustaka yang terpasang."""
    global _DEFAULT_PARAMS_CACHE
    if _DEFAULT_PARAMS_CACHE is not None:
        return dict(_DEFAULT_PARAMS_CACHE)

    fallback = {"learning_rate": 0.3, "max_depth": 6, "n_estimators": 100}

    try:
        import json as _json

        rng = np.random.default_rng(0)
        X_probe = rng.normal(size=(64, 4))
        y_probe = (X_probe[:, 0] > 0).astype(int)

        probe = xgb.XGBClassifier()
        probe.fit(X_probe, y_probe)

        booster = probe.get_booster()
        config = _json.loads(booster.save_config())

        def cari(obj: Any, kunci: str) -> Any:
            """Telusuri konfigurasi bersarang untuk menemukan satu kunci."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k == kunci and not isinstance(v, (dict, list)):
                        return v
                    hasil = cari(v, kunci)
                    if hasil is not None:
                        return hasil
            elif isinstance(obj, list):
                for item in obj:
                    hasil = cari(item, kunci)
                    if hasil is not None:
                        return hasil
            return None

        eta = cari(config, "eta")
        depth = cari(config, "max_depth")

        _DEFAULT_PARAMS_CACHE = {
            # eta disimpan sebagai float32 (0.300000012) — dibulatkan agar rapi
            "learning_rate": round(float(eta), 4) if eta is not None else fallback["learning_rate"],
            "max_depth": int(depth) if depth is not None else fallback["max_depth"],
            "n_estimators": int(booster.num_boosted_rounds()),
            "source": f"dibaca dari pustaka xgboost {xgb.__version__}",
        }
    except Exception:
        _DEFAULT_PARAMS_CACHE = {**fallback, "source": "nilai cadangan (gagal membaca pustaka)"}

    return dict(_DEFAULT_PARAMS_CACHE)


DEFAULT_PARAMS = {
    "learning_rate": 0.3,
    "max_depth": 6,
    "n_estimators": 100,
}

# Nilai yang SELAMA INI DIPAPARKAN sebagai hasil optimasi SGO
# (lihat ml-engine/artifacts/model_metadata.json dan halaman Perbandingan Model).
# Nilai-nilai inilah yang hendak dibuktikan kebenarannya.
CLAIMED_SGO_PARAMS = {
    "learning_rate": 0.035,
    "max_depth": 9,
    "n_estimators": 285,
}

# Toleransi ketika membandingkan nilai temuan SGO dengan nilai yang dipaparkan.
# Dinyatakan sebagai proporsi terhadap lebar ruang pencarian tiap parameter,
# sehingga adil untuk parameter dengan skala berbeda.
MATCH_TOLERANCE_RATIO = 0.10


# --------------------------------------------------------------------- data
def load_dataset(
    path: Path | str = DATASET_PATH,
    include_blood_pressure: bool = False,
) -> tuple[np.ndarray, np.ndarray, List[str]]:
    """Membaca dataset dan mengubahnya menjadi matriks fitur + vektor target."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan di {path}. "
            "Salin berkas CSV ke ml-engine/data/dataset_hipertensi.csv."
        )

    df = pd.read_csv(path)

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Kolom target '{TARGET_COLUMN}' tidak ada pada dataset.")

    # Jenis kelamin disimpan sebagai teks pada sebagian berkas
    if df["Jenis_Kelamin"].dtype == object:
        df["Jenis_Kelamin"] = df["Jenis_Kelamin"].map({"Laki-laki": 1, "Perempuan": 0})

    excluded = list(DROP_COLUMNS)
    if not include_blood_pressure:
        excluded += BLOOD_PRESSURE_COLUMNS

    feature_columns = [c for c in df.columns if c not in excluded]

    X = df[feature_columns].astype(float).to_numpy()
    y = df[TARGET_COLUMN].astype(int).to_numpy()

    return X, y, feature_columns


def _split(X: np.ndarray, y: np.ndarray, seed: int):
    """Bagi menjadi 60% latih, 20% validasi, 20% uji (stratified)."""
    X_train, X_tmp, y_train, y_tmp = train_test_split(
        X, y, test_size=0.4, random_state=seed, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_tmp, y_tmp, test_size=0.5, random_state=seed, stratify=y_tmp
    )
    return X_train, y_train, X_val, y_val, X_test, y_test


# ------------------------------------------------------------------ metrics
def _evaluate_model(model: xgb.XGBClassifier, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
    """Hitung metrik pada data uji sekaligus mengukur waktu inferensi nyata."""
    started = time.perf_counter()
    y_pred = model.predict(X_test)
    inference_total_ms = (time.perf_counter() - started) * 1000.0

    try:
        y_proba = model.predict_proba(X_test)[:, 1]
        auc = float(roc_auc_score(y_test, y_proba))
    except Exception:
        auc = None

    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

    return {
        "accuracy": round(float(accuracy_score(y_test, y_pred)) * 100, 2),
        "precision": round(float(precision_score(y_test, y_pred, average="macro", zero_division=0)) * 100, 2),
        "recall": round(float(recall_score(y_test, y_pred, average="macro", zero_division=0)) * 100, 2),
        "f1": round(float(f1_score(y_test, y_pred, average="macro", zero_division=0)) * 100, 2),
        "auc": round(auc * 100, 2) if auc is not None else None,
        "confusion_matrix": cm.tolist(),
        "inference_total_ms": round(inference_total_ms, 2),
        "inference_per_sample_ms": round(inference_total_ms / max(len(X_test), 1), 4),
    }


def _build_model(params: Dict[str, Any], seed: int) -> xgb.XGBClassifier:
    """Bangun XGBoost. Hanya tiga parameter yang berubah; sisanya dibiarkan bawaan."""
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


def _train_and_score(
    params: Dict[str, Any],
    label: str,
    seed: int,
    X_train, y_train, X_test, y_test,
) -> Dict[str, Any]:
    """Latih satu model lalu ukur metrik dan waktunya pada data uji."""
    model = _build_model(params, seed)

    started = time.perf_counter()
    model.fit(X_train, y_train)
    train_s = time.perf_counter() - started

    return {
        "label": label,
        "hyperparameters": {
            "learning_rate": round(float(params["learning_rate"]), 4),
            "max_depth": int(params["max_depth"]),
            "n_estimators": int(params["n_estimators"]),
        },
        "metrics": _evaluate_model(model, X_test, y_test),
        "timing": {"training_s": round(train_s, 3)},
    }


def _verify_claim(found: Dict[str, Any]) -> Dict[str, Any]:
    """
    Bandingkan nilai temuan SGO dengan nilai yang selama ini dipaparkan.

    Sebuah parameter dianggap "cocok" bila selisihnya masih dalam
    MATCH_TOLERANCE_RATIO dari lebar ruang pencarian parameter tersebut.
    """
    bounds = {s.name: (s.low, s.high) for s in SEARCH_SPACE}
    rows = []

    for name in TUNED_PARAMETERS:
        low, high = bounds[name]
        claimed = CLAIMED_SGO_PARAMS[name]
        actual = found[name]

        diff = abs(float(actual) - float(claimed))
        tolerance = (high - low) * MATCH_TOLERANCE_RATIO

        rows.append({
            "parameter": name,
            "claimed": claimed,
            "found": round(float(actual), 4) if name == "learning_rate" else int(actual),
            "difference": round(diff, 4),
            "tolerance": round(tolerance, 4),
            "match": bool(diff <= tolerance),
            "search_range": [low, high],
        })

    n_match = sum(1 for r in rows if r["match"])

    if n_match == len(rows):
        verdict = "cocok"
        summary = (
            "Seluruh nilai yang dipaparkan berhasil direproduksi oleh SGO pada "
            "percobaan ini (dalam batas toleransi)."
        )
    elif n_match == 0:
        verdict = "tidak cocok"
        summary = (
            "Tidak satu pun nilai yang dipaparkan berhasil direproduksi. Nilai "
            "0.035 / 9 / 285 tidak muncul dari proses optimasi ini."
        )
    else:
        verdict = "sebagian"
        summary = (
            f"{n_match} dari {len(rows)} nilai yang dipaparkan berhasil "
            "direproduksi; sisanya berbeda."
        )

    return {
        "parameters": rows,
        "matched_count": n_match,
        "total_count": len(rows),
        "verdict": verdict,
        "summary": summary,
    }


# ------------------------------------------- pembanding waktu pada iterasi sama
def run_timing_comparison(
    default_iterations: int = 100,
    optimized_iterations: int = 100,
    seed: int = 42,
    include_blood_pressure: bool = False,
    repeats: int = 3,
    dataset_path: Path | str = DATASET_PATH,
) -> Dict[str, Any]:
    """
    Bandingkan waktu eksekusi dan akurasi dua model pada JUMLAH ITERASI BOOSTING
    yang ditentukan sendiri untuk masing-masing model.

    Yang dimaksud "iterasi" di sini adalah `n_estimators` — banyaknya putaran
    boosting, yaitu jumlah pohon yang dibangun. Ini berbeda dari "iterasi SGO"
    yang merupakan jumlah generasi pada proses pencarian hyperparameter.

    Mengapa perlu disamakan? Pada perbandingan sebelumnya model default memakai
    100 pohon sementara model hasil optimasi memakai jumlah lain, sehingga
    selisih waktunya lebih mencerminkan perbedaan jumlah pohon daripada
    perbedaan mutu konfigurasi. Dengan menyamakan jumlah iterasi, yang terukur
    murni pengaruh `learning_rate` dan `max_depth`.

    Pelatihan diulang `repeats` kali lalu diambil nilai TENGAH (median), karena
    pengukuran waktu satu kali jalan mudah terganggu beban lain pada komputer.
    """
    overall_started = time.perf_counter()

    X, y, feature_columns = load_dataset(dataset_path, include_blood_pressure)
    X_train, y_train, X_val, y_val, X_test, y_test = _split(X, y, seed)

    library_defaults = _library_default_params()
    library_defaults.pop("source", None)

    susunan = [
        {
            "key": "default",
            "label": "XGBoost Default",
            "params": {
                "learning_rate": library_defaults["learning_rate"],
                "max_depth": library_defaults["max_depth"],
                "n_estimators": int(default_iterations),
            },
            "note": "learning_rate & max_depth memakai nilai bawaan pustaka XGBoost",
        },
        {
            "key": "optimized",
            "label": "XGBoost + SGO (nilai dipaparkan)",
            "params": {
                "learning_rate": CLAIMED_SGO_PARAMS["learning_rate"],
                "max_depth": CLAIMED_SGO_PARAMS["max_depth"],
                "n_estimators": int(optimized_iterations),
            },
            "note": "learning_rate & max_depth memakai nilai hasil optimasi yang dipaparkan",
        },
    ]

    hasil_model = []

    for item in susunan:
        durasi_latih: List[float] = []
        model = None

        for _ in range(max(repeats, 1)):
            kandidat = _build_model(item["params"], seed)
            mulai = time.perf_counter()
            kandidat.fit(X_train, y_train)
            durasi_latih.append(time.perf_counter() - mulai)
            model = kandidat

        metrik = _evaluate_model(model, X_test, y_test)

        hasil_model.append({
            "key": item["key"],
            "label": item["label"],
            "note": item["note"],
            "hyperparameters": {
                "learning_rate": round(float(item["params"]["learning_rate"]), 4),
                "max_depth": int(item["params"]["max_depth"]),
                "n_estimators": int(item["params"]["n_estimators"]),
            },
            "metrics": metrik,
            "timing": {
                "training_median_s": round(float(np.median(durasi_latih)), 4),
                "training_min_s": round(float(np.min(durasi_latih)), 4),
                "training_max_s": round(float(np.max(durasi_latih)), 4),
                "training_per_tree_ms": round(
                    float(np.median(durasi_latih)) * 1000 / max(int(item["params"]["n_estimators"]), 1), 4
                ),
                "inference_total_ms": metrik["inference_total_ms"],
                "inference_per_sample_ms": metrik["inference_per_sample_ms"],
            },
        })

    d, o = hasil_model[0], hasil_model[1]
    selisih_latih = o["timing"]["training_median_s"] - d["timing"]["training_median_s"]

    return {
        "dataset": {
            "path": str(Path(dataset_path).name),
            "total_samples": int(len(y)),
            "n_features": len(feature_columns),
            "include_blood_pressure": include_blood_pressure,
            "feature_set_note": FEATURE_SET_DESCRIPTION[include_blood_pressure],
            "majority_baseline": round(float(max(np.mean(y_test), 1 - np.mean(y_test))) * 100, 2),
            "split": {
                "train": int(len(y_train)),
                "validation": int(len(y_val)),
                "test": int(len(y_test)),
            },
        },
        "config": {
            "default_iterations": int(default_iterations),
            "optimized_iterations": int(optimized_iterations),
            "same_iterations": int(default_iterations) == int(optimized_iterations),
            "repeats": max(repeats, 1),
            "seed": seed,
            "iteration_meaning": (
                "n_estimators — jumlah putaran boosting (jumlah pohon), "
                "bukan iterasi pencarian SGO"
            ),
        },
        "models": hasil_model,
        "comparison": {
            "accuracy_diff": round(o["metrics"]["accuracy"] - d["metrics"]["accuracy"], 2),
            "f1_diff": round(o["metrics"]["f1"] - d["metrics"]["f1"], 2),
            "training_diff_s": round(selisih_latih, 4),
            "training_ratio": round(
                o["timing"]["training_median_s"] / max(d["timing"]["training_median_s"], 1e-9), 2
            ),
            "inference_diff_ms": round(
                o["timing"]["inference_total_ms"] - d["timing"]["inference_total_ms"], 3
            ),
            "faster_model": d["label"] if selisih_latih > 0 else o["label"],
        },
        "total_runtime_s": round(time.perf_counter() - overall_started, 3),
    }


# ---------------------------------------------------------------- pembanding
def run_comparison(
    iterations: int = 10,
    population_size: int = 6,
    seed: int = 42,
    include_blood_pressure: bool = False,
    verification_runs: int = 1,
    dataset_path: Path | str = DATASET_PATH,
    on_iteration: Optional[Callable[[IterationRecord], None]] = None,
) -> Dict[str, Any]:
    """
    Jalankan pembuktian penuh dan kembalikan hasilnya sebagai dict siap-JSON.

    Tiga model dibandingkan pada data uji yang sama:
      1. XGBoost Default            - nilai bawaan pustaka (0.3 / 6 / 100)
      2. Nilai yang Dipaparkan      - 0.035 / 9 / 285 sesuai laporan
      3. Hasil SGO saat ini         - apa pun yang ditemukan algoritma

    `iterations` dan `population_size` diatur bebas oleh pengguna.
    `verification_runs` mengulang optimasi dengan seed berbeda untuk melihat
    apakah SGO konsisten mengarah ke nilai yang dipaparkan.
    """
    overall_started = time.perf_counter()

    X, y, feature_columns = load_dataset(dataset_path, include_blood_pressure)
    X_train, y_train, X_val, y_val, X_test, y_test = _split(X, y, seed)

    # --------------------------------------------- 1. Model pembanding tetap
    # Nilai bawaan dibaca dari pustaka XGBoost, bukan diketik di dalam kode.
    library_defaults = _library_default_params()
    default_source = library_defaults.pop("source", "")

    default_result = _train_and_score(
        library_defaults, "XGBoost Default", seed, X_train, y_train, X_test, y_test
    )
    claimed_result = _train_and_score(
        CLAIMED_SGO_PARAMS, "Nilai yang Dipaparkan", seed, X_train, y_train, X_test, y_test
    )
    default_train_s = default_result["timing"]["training_s"]
    default_metrics = default_result["metrics"]

    # -------------------------------------------------------- 2. Optimasi SGO
    # Fitness = macro F1 pada data VALIDASI (bukan data uji), supaya metrik akhir
    # tetap diukur pada data yang belum pernah dilihat selama optimasi.
    #
    # Sengaja memakai macro F1, BUKAN accuracy. Kelas pada dataset ini timpang
    # (65% berisiko), sehingga bila fitness memakai accuracy, SGO akan menemukan
    # "jalan pintas": model yang selalu menebak kelas mayoritas sudah mendapat
    # akurasi 65% tanpa benar-benar belajar. Macro F1 menghukum solusi malas
    # tersebut karena mengharuskan kedua kelas dikenali dengan baik.
    def fitness(params: Dict[str, float]) -> float:
        model = _build_model(params, seed)
        model.fit(X_train, y_train)
        return float(f1_score(y_val, model.predict(X_val), average="macro", zero_division=0))

    optimizer = SocialGroupOptimizer(
        space=SEARCH_SPACE,
        fitness_fn=fitness,
        population_size=population_size,
        iterations=iterations,
        seed=seed,
    )

    sgo_result = optimizer.optimize(on_iteration=on_iteration)
    best_params = {name: sgo_result.best_params[name] for name in TUNED_PARAMETERS}

    # ------------------------------------------- 3. Latih ulang dengan hasil SGO
    sgo_scored = _train_and_score(
        best_params, "XGBoost + SGO", seed, X_train, y_train, X_test, y_test
    )
    sgo_train_s = sgo_scored["timing"]["training_s"]
    sgo_metrics = sgo_scored["metrics"]

    # -------------------------------- 4. Uji reproduksibilitas (seed berbeda)
    # Menjawab pertanyaan: apakah SGO KONSISTEN mengarah ke nilai yang
    # dipaparkan, atau nilainya berpindah-pindah setiap kali dijalankan?
    reproducibility: List[Dict[str, Any]] = [
        {
            "seed": seed,
            "learning_rate": round(float(best_params["learning_rate"]), 4),
            "max_depth": int(best_params["max_depth"]),
            "n_estimators": int(best_params["n_estimators"]),
            "validation_f1": round(sgo_result.best_fitness * 100, 2),
        }
    ]

    for extra in range(1, max(verification_runs, 1)):
        alt_seed = seed + extra * 7
        alt_optimizer = SocialGroupOptimizer(
            space=SEARCH_SPACE,
            fitness_fn=fitness,
            population_size=population_size,
            iterations=iterations,
            seed=alt_seed,
        )
        alt = alt_optimizer.optimize()
        reproducibility.append({
            "seed": alt_seed,
            "learning_rate": round(float(alt.best_params["learning_rate"]), 4),
            "max_depth": int(alt.best_params["max_depth"]),
            "n_estimators": int(alt.best_params["n_estimators"]),
            "validation_f1": round(alt.best_fitness * 100, 2),
        })

    # ------------------------------------------------------------- 5. Rangkuman
    total_s = time.perf_counter() - overall_started

    return {
        "dataset": {
            "path": str(Path(dataset_path).name),
            "total_samples": int(len(y)),
            "n_features": len(feature_columns),
            "features": feature_columns,
            "include_blood_pressure": include_blood_pressure,
            "feature_set_note": FEATURE_SET_DESCRIPTION[include_blood_pressure],
            # Akurasi bila model asal menebak kelas terbanyak. Dipakai sebagai
            # pembanding kejujuran: model yang berada di bawah angka ini berarti
            # belum belajar apa pun yang berguna.
            "majority_baseline": round(
                float(max(np.mean(y_test), 1 - np.mean(y_test))) * 100, 2
            ),
            "class_names": CLASS_NAMES,
            "class_distribution": {
                CLASS_NAMES[0]: int((y == 0).sum()),
                CLASS_NAMES[1]: int((y == 1).sum()),
            },
            "split": {
                "train": int(len(y_train)),
                "validation": int(len(y_val)),
                "test": int(len(y_test)),
            },
        },
        "config": {
            "iterations": iterations,
            "population_size": population_size,
            "seed": seed,
            "verification_runs": max(verification_runs, 1),
            "total_model_trainings": sgo_result.n_evaluations,
            "tuned_parameters": TUNED_PARAMETERS,
        },
        "default": {
            **default_result,
            "source": default_source,
            "note": (
                "Nilai ini bukan pilihan peneliti, melainkan bawaan pustaka "
                "XGBoost yang dibaca langsung dari konfigurasi booster saat "
                "program berjalan."
            ),
            "timing": {
                "optimization_s": 0.0,
                "training_s": default_train_s,
                "total_s": default_train_s,
            },
        },
        "claimed": {
            **claimed_result,
            "note": (
                "Nilai ini TIDAK dicari oleh algoritma — inilah angka yang selama "
                "ini dituliskan pada laporan dan metadata model, dilatih ulang "
                "apa adanya sebagai pembanding."
            ),
        },
        "sgo": {
            **sgo_scored,
            "validation_fitness": round(sgo_result.best_fitness * 100, 2),
            "fitness_metric": "macro F1 pada data validasi",
            "timing": {
                "optimization_s": round(sgo_result.elapsed_s, 3),
                "training_s": sgo_train_s,
                "total_s": round(sgo_result.elapsed_s + sgo_train_s, 3),
            },
        },
        "verification": _verify_claim(best_params),
        "reproducibility": reproducibility,
        "improvement": {
            "accuracy": round(sgo_metrics["accuracy"] - default_metrics["accuracy"], 2),
            "precision": round(sgo_metrics["precision"] - default_metrics["precision"], 2),
            "recall": round(sgo_metrics["recall"] - default_metrics["recall"], 2),
            "f1": round(sgo_metrics["f1"] - default_metrics["f1"], 2),
            "extra_time_s": round(
                (sgo_result.elapsed_s + sgo_train_s) - default_train_s, 3
            ),
        },
        # Selisih model "nilai yang dipaparkan" terhadap default — untuk menilai
        # apakah angka 0.035 / 9 / 285 memang membawa perbaikan seperti diklaim.
        "claimed_improvement": {
            "accuracy": round(
                claimed_result["metrics"]["accuracy"] - default_metrics["accuracy"], 2
            ),
            "f1": round(claimed_result["metrics"]["f1"] - default_metrics["f1"], 2),
        },
        "convergence": [
            {
                "iteration": r.iteration,
                "best_fitness": round(r.best_fitness * 100, 3),
                "mean_fitness": round(r.mean_fitness * 100, 3),
                "elapsed_s": r.elapsed_s,
            }
            for r in sgo_result.history
        ],
        "total_runtime_s": round(total_s, 3),
    }
