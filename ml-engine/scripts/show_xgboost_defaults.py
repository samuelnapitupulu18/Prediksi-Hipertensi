"""
Bukti Asal-usul Nilai Bawaan XGBoost
====================================

Skrip ini SENGAJA tidak menuliskan angka apa pun di dalam kodenya.

Setiap nilai yang tampil di layar diambil saat itu juga dari:
  (a) berkas metadata yang dibuat pip ketika paket dipasang, dan
  (b) konfigurasi internal XGBoost yang dikeluarkan oleh pustaka itu sendiri.

Untuk tiap bukti, perintah yang dijalankan dicetak lebih dulu, disusul
keluaran MENTAHNYA tanpa diubah. Dengan begitu pembaca dapat mengetik ulang
perintah yang sama dan membandingkan hasilnya.

CARA MENJALANKAN
----------------
    cd ml-engine
    .venv\\Scripts\\python.exe scripts/show_xgboost_defaults.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import xgboost as xgb

GARIS = "=" * 78


def judul(teks: str) -> None:
    print()
    print(GARIS)
    print(f" {teks}")
    print(GARIS)


def perintah(kode: str) -> None:
    """Cetak potongan kode yang akan dijalankan, sebelum keluarannya muncul."""
    print()
    for baris in kode.strip().splitlines():
        print(f"    >>> {baris.strip()}")
    print()


def main() -> int:
    print(GARIS)
    print(" BUKTI ASAL-USUL NILAI BAWAAN XGBoost")
    print(" Tidak ada angka yang ditulis di dalam skrip ini — semuanya dibaca")
    print(" langsung dari pustaka dan berkas metadata paket.")
    print(GARIS)

    # ══════════════════════════════════════════════════════════ BUKTI 1
    judul("BUKTI 1 — Identitas paket, dibaca dari pustaka yang terpasang")
    perintah("""
import xgboost
xgboost.__version__
xgboost.__file__
""")
    print(f"    {xgb.__version__!r}")
    print(f"    {xgb.__file__!r}")

    # ══════════════════════════════════════════════════════════ BUKTI 2
    dist = Path(xgb.__file__).parent.parent / f"xgboost-{xgb.__version__}.dist-info"
    metadata = dist / "METADATA"
    installer = dist / "INSTALLER"

    judul("BUKTI 2 — Isi berkas METADATA (dibuat pip saat pemasangan)")
    print(f" Berkas: {metadata}")
    perintah(f"type {metadata.name}")

    if metadata.exists():
        pola = re.compile(r"^(Name|Version|License|Project-URL|Author-email|Requires-Python):")
        for baris in metadata.read_text(encoding="utf-8", errors="ignore").splitlines():
            if pola.match(baris):
                print(f"    {baris}")
    else:
        print("    (berkas tidak ditemukan)")

    if installer.exists():
        print()
        print(f" Berkas: {installer.name}  ->  {installer.read_text(encoding='utf-8').strip()!r}")
        print("    (menandakan paket dipasang memakai pip dari PyPI)")

    # ══════════════════════════════════════════════════════════ BUKTI 3
    judul("BUKTI 3 — XGBClassifier() tanpa parameter: apa isi get_params()?")
    perintah("""
from xgboost import XGBClassifier
p = XGBClassifier().get_params()
{k: p[k] for k in ('learning_rate', 'max_depth', 'n_estimators')}
""")
    params = xgb.XGBClassifier().get_params()
    subset = {k: params.get(k) for k in ("learning_rate", "max_depth", "n_estimators")}
    print(f"    {subset}")
    print()
    print(" Nilainya None. Sejak XGBoost 2.x penetapan nilai diserahkan kepada")
    print(" inti C++, sehingga baru terlihat setelah model dilatih -> Bukti 4.")

    # ══════════════════════════════════════════════════════════ BUKTI 4
    judul("BUKTI 4 — Konfigurasi mentah yang dikeluarkan XGBoost setelah dilatih")
    perintah("""
model = XGBClassifier()
model.fit(X, y)
json.loads(model.get_booster().save_config())
""")

    rng = np.random.default_rng(0)
    X = rng.normal(size=(64, 4))
    y = (X[:, 0] > 0).astype(int)

    model = xgb.XGBClassifier()
    model.fit(X, y)

    booster = model.get_booster()
    config = json.loads(booster.save_config())

    # Cetak blok MENTAH dari konfigurasi pustaka, utuh dan apa adanya.
    gb = config["learner"]["gradient_booster"]

    print(" [mentah] gbtree_model_param — memuat jumlah pohon:")
    print()
    for baris in json.dumps(gb["gbtree_model_param"], indent=2).splitlines():
        print(f"    {baris}")

    tree_param = None
    for kandidat in ("tree_train_param", "train_param"):
        if kandidat in gb:
            tree_param = gb[kandidat]
            break
    if tree_param is None and isinstance(gb.get("updater"), list) and gb["updater"]:
        tree_param = next(
            (v for v in gb["updater"][0].values() if isinstance(v, dict)), None
        )

    if tree_param:
        # Hanya parameter yang relevan agar mudah dibaca, nilainya tetap mentah.
        relevan = {
            k: v for k, v in tree_param.items()
            if k in ("eta", "learning_rate", "max_depth", "min_child_weight",
                     "subsample", "colsample_bytree", "gamma", "lambda", "alpha")
        }
        print()
        print(" [mentah] tree_train_param — memuat eta dan max_depth:")
        print()
        for baris in json.dumps(relevan, indent=2).splitlines():
            print(f"    {baris}")

    def cari(obj, kunci):
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
    max_depth = cari(config, "max_depth")
    n_trees = booster.num_boosted_rounds()

    print()
    print(" Nilai yang diambil dari konfigurasi di atas:")
    print(f"    eta                              = {eta!r}")
    print(f"    max_depth                        = {max_depth!r}")
    print(f"    booster.num_boosted_rounds()     = {n_trees!r}")

    # ══════════════════════════════════════════════════════════ RINGKASAN
    judul("RINGKASAN")
    print(f"    learning_rate  = {round(float(eta), 4)}")
    print(f"    max_depth      = {int(max_depth)}")
    print(f"    n_estimators   = {int(n_trees)}")
    print()
    print(" Ketiganya berasal dari pustaka, bukan dari peneliti. Nilai inilah")
    print(" yang dipakai sebagai pembanding 'XGBoost Default' pada eksperimen.")

    # ══════════════════════════════════════════════════════════ VERIFIKASI
    judul("VERIFIKASI MANDIRI — tanpa perlu mempercayai skrip ini")
    print(" Salin-tempel perintah berikut ke terminal. Hasilnya harus sama.")
    print()
    print(' 1) Versi dan lokasi pustaka:')
    print('    .venv\\Scripts\\python.exe -c "import xgboost;print(xgboost.__version__, xgboost.__file__)"')
    print()
    print(' 2) Nilai bawaan langsung dari pustaka:')
    print('    .venv\\Scripts\\python.exe -c "import xgboost,json,numpy as np;'
          'm=xgboost.XGBClassifier();X=np.random.rand(50,3);'
          'm.fit(X,(X[:,0]>0.5).astype(int));'
          'c=json.loads(m.get_booster().save_config());'
          'print(json.dumps(c[\'learner\'][\'gradient_booster\'],indent=1)[:400])"')
    print()
    print(' 3) Dokumentasi resmi (bandingkan angkanya):')
    print("    https://xgboost.readthedocs.io/en/stable/parameter.html")
    print("    https://xgboost.readthedocs.io/en/stable/python/python_api.html")
    print()
    print(' 4) Kode sumber tempat nilai bawaan ditetapkan:')
    print("    https://github.com/dmlc/xgboost")
    print(GARIS)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
