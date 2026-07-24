"""
Eksperimen SGO — versi baris perintah (tanpa web)
=================================================

Menjalankan pembuktian yang sama persis dengan halaman "Uji Prediksi Live",
tetapi berdiri sendiri: tidak perlu menyalakan backend, frontend, maupun
database. Cocok dipakai sebagai lampiran skripsi karena hasilnya dapat
direproduksi siapa pun hanya dengan Python.

TIDAK ADA BATAS ITERASI di sini. Batas 500 pada antarmuka web semata-mata
penjagaan agar permintaan HTTP tidak melampaui waktu tunggu.

CONTOH PEMAKAIAN
----------------
    # Percobaan cepat
    .venv\\Scripts\\python.exe scripts/run_sgo_experiment.py --iterations 10

    # Percobaan panjang dengan 5 pengulangan seed
    .venv\\Scripts\\python.exe scripts/run_sgo_experiment.py \\
        --iterations 100 --population 10 --runs 5

    # Sertakan tekanan darah sebagai fitur
    .venv\\Scripts\\python.exe scripts/run_sgo_experiment.py --with-bp

    # Simpan hasil mentah untuk lampiran
    .venv\\Scripts\\python.exe scripts/run_sgo_experiment.py \\
        --iterations 50 --runs 3 --output hasil_eksperimen.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Agar modul `app` dapat diimpor saat skrip dijalankan langsung
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.optimization.benchmark import run_comparison  # noqa: E402
from app.optimization.sgo import IterationRecord  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Pembuktian XGBoost Default vs Nilai yang Dipaparkan vs XGBoost + SGO",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--iterations", type=int, default=10, help="Jumlah iterasi SGO (bebas)")
    p.add_argument("--population", type=int, default=6, help="Ukuran populasi SGO")
    p.add_argument("--seed", type=int, default=42, help="Seed acak")
    p.add_argument("--runs", type=int, default=1, help="Pengulangan dengan seed berbeda")
    p.add_argument("--with-bp", action="store_true", help="Sertakan TDS & TDD sebagai fitur")
    p.add_argument("--output", type=str, default=None, help="Simpan hasil lengkap ke berkas JSON")
    p.add_argument("--quiet", action="store_true", help="Sembunyikan kemajuan per iterasi")
    return p.parse_args()


def garis(char: str = "=", n: int = 78) -> str:
    return char * n


def main() -> int:
    args = parse_args()

    if args.iterations < 1 or args.population < 3:
        print("iterations minimal 1 dan population minimal 3.", file=sys.stderr)
        return 1

    per_run = args.population + args.iterations * args.population * 2
    total = per_run * max(args.runs, 1)

    print(garis())
    print(" PEMBUKTIAN NILAI HYPERPARAMETER — XGBoost Default vs Dipaparkan vs SGO")
    print(garis())
    print(f" Iterasi          : {args.iterations}")
    print(f" Populasi         : {args.population}")
    print(f" Seed             : {args.seed}")
    print(f" Pengulangan seed : {args.runs}")
    print(f" Mode fitur       : {'dengan tekanan darah' if args.with_bp else 'tanpa tekanan darah'}")
    print(f" Perkiraan beban  : {total} pelatihan model (± {total * 0.15:.0f} detik)")
    print(garis())
    print()

    def on_iteration(rec: IterationRecord) -> None:
        if not args.quiet:
            print(
                f"  iterasi {rec.iteration:>4}/{args.iterations}  "
                f"fitness terbaik {rec.best_fitness * 100:6.3f}%  "
                f"rata-rata {rec.mean_fitness * 100:6.3f}%  "
                f"({rec.elapsed_s:.2f}s)"
            )

    started = time.perf_counter()
    hasil = run_comparison(
        iterations=args.iterations,
        population_size=args.population,
        seed=args.seed,
        include_blood_pressure=args.with_bp,
        verification_runs=args.runs,
        on_iteration=on_iteration,
    )
    durasi = time.perf_counter() - started

    ds = hasil["dataset"]
    print()
    print(garis())
    print(" DATASET")
    print(garis("-"))
    print(f" Berkas            : {ds['path']}")
    print(f" Jumlah sampel     : {ds['total_samples']:,}".replace(",", "."))
    print(f" Jumlah fitur      : {ds['n_features']}  ({', '.join(ds['features'])})")
    print(f" Pembagian         : {ds['split']['train']} latih / "
          f"{ds['split']['validation']} validasi / {ds['split']['test']} uji")
    print(f" Kelas             : {ds['class_names'][0]} = {ds['class_distribution'][ds['class_names'][0]]}, "
          f"{ds['class_names'][1]} = {ds['class_distribution'][ds['class_names'][1]]}")
    print(f" Baseline mayoritas: {ds['majority_baseline']}%")
    print()

    print(garis())
    print(" PERFORMA KETIGA MODEL (data uji)")
    print(garis("-"))
    print(f" {'Model':<24}{'lr':>8}{'depth':>7}{'trees':>7}{'Acc':>9}{'F1':>9}{'Latih':>9}")
    print(garis("-"))
    for kunci in ("default", "claimed", "sgo"):
        m = hasil[kunci]
        h = m["hyperparameters"]
        print(
            f" {m['label']:<24}{h['learning_rate']:>8}{h['max_depth']:>7}{h['n_estimators']:>7}"
            f"{m['metrics']['accuracy']:>8.2f}%{m['metrics']['f1']:>8.2f}%"
            f"{m['timing']['training_s']:>8.3f}s"
        )
    print()

    v = hasil["verification"]
    print(garis())
    print(f" HASIL PEMBUKTIAN : {v['verdict'].upper()}")
    print(garis("-"))
    print(f" {v['summary']}")
    print()
    print(f" {'Parameter':<18}{'Dipaparkan':>12}{'Ditemukan':>12}{'Selisih':>12}{'Toleransi':>12}  Status")
    print(garis("-"))
    for p in v["parameters"]:
        status = "COCOK" if p["match"] else "TIDAK COCOK"
        print(
            f" {p['parameter']:<18}{str(p['claimed']):>12}{str(p['found']):>12}"
            f"{p['difference']:>12}{p['tolerance']:>12}  {status}"
        )
    print()

    if len(hasil["reproducibility"]) > 1:
        print(garis())
        print(" UJI KONSISTENSI ANTAR SEED")
        print(garis("-"))
        print(f" {'Seed':>6}{'learning_rate':>16}{'max_depth':>12}{'n_estimators':>14}{'F1 validasi':>14}")
        print(garis("-"))
        for r in hasil["reproducibility"]:
            print(
                f" {r['seed']:>6}{r['learning_rate']:>16}{r['max_depth']:>12}"
                f"{r['n_estimators']:>14}{r['validation_f1']:>13.2f}%"
            )
        print()

    print(garis())
    print(" WAKTU")
    print(garis("-"))
    print(f" Optimasi SGO      : {hasil['sgo']['timing']['optimization_s']} detik "
          f"({hasil['config']['total_model_trainings']} pelatihan model)")
    print(f" Latih default     : {hasil['default']['timing']['training_s']} detik")
    print(f" Biaya tambahan    : +{hasil['improvement']['extra_time_s']} detik")
    print(f" Total keseluruhan : {durasi:.1f} detik")
    print(garis())

    if args.output:
        out = Path(args.output)
        out.write_text(json.dumps(hasil, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nHasil lengkap disimpan ke: {out.resolve()}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
