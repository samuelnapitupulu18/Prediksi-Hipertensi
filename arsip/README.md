# Arsip — Berkas Lama yang TIDAK Boleh Dipakai Lagi

Folder ini menyimpan berkas dari tahap pengembangan awal yang **menghasilkan
angka tidak sah**. Semuanya sudah **tidak dipakai** oleh sistem. Berkasnya
disimpan (bukan dihapus) agar riwayat pengerjaan tetap utuh dan dapat
dipertanggungjawabkan bila ditanyakan.

**Jangan menjalankan atau menampilkan berkas di folder ini saat sidang.**

---

## `simulasi_seminar.py`

Skrip evaluasi yang **memalsukan hasil**.

Skrip ini memang melatih dua model XGBoost, tetapi hasil prediksi keduanya
**dibuang**. Fungsi `generator_prediksi_dinamis()` mengambil jawaban benar
(`y_test`) lalu sengaja merusak sebagian tepat sebanyak yang diperlukan agar
akurasinya jatuh persis pada angka target yang ditulis di baris 62–63:

```python
acc_default_target = 82.45
acc_sgo_target     = 93.27
```

Selain itu, label tiga kelas pada skrip ini dibangkitkan acak lalu diacak lagi
(`np.random.shuffle`), sehingga tidak memiliki kaitan apa pun dengan fitur.
Model yang dilatih sungguhan pada label semacam itu akan memperoleh akurasi
sekitar 33% (setara menebak).

**Pengganti:** `ml-engine/scripts/run_sgo_experiment.py` — menjalankan optimasi
SGO yang sesungguhnya dan melaporkan angka hasil pengukuran nyata.

## `simulasi.py`

Versi lebih awal dari skrip di atas, dengan persoalan yang sama.

## `generate_mock_model.py`

Pembuat model produksi versi lama. Model dilatih dari
`sklearn.datasets.make_classification` — **data acak sintetis yang tidak ada
hubungannya dengan hipertensi**. Metadata yang dihasilkannya pun menyatakan
dirinya sendiri sebagai tiruan:

```json
"version": "1.0.0-sgo-mock",
"optimization": "Social Group Optimization (SGO) - MOCK",
"description": "This is a synthetic dummy model generated for testing the API."
```

Hyperparameter `learning_rate 0.035`, `max_depth 9`, `n_estimators 285` pada
skrip itu **diketik langsung**, disalin dari dokumen — bukan hasil pencarian
algoritma.

**Pengganti:** `ml-engine/scripts/train_production_model.py` — melatih model
dari dataset hipertensi asli, memakai pipeline pra-pemrosesan yang sama dengan
inferensi, dengan hyperparameter yang benar-benar dicari memakai SGO.

---

## Bila ditanya penguji

Sampaikan apa adanya: berkas-berkas ini berasal dari tahap awal pengembangan
ketika sistem masih dirangkai dan model sungguhan belum dilatih. Setelah
diperiksa ulang, seluruhnya diganti dengan proses yang dapat direproduksi, dan
berkas lamanya diarsipkan secara terbuka di sini. Rincian penggantinya ada pada
[EKSPERIMEN_SGO.md](../docs/EKSPERIMEN_SGO.md).
