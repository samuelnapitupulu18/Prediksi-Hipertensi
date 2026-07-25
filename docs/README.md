# Indeks Dokumentasi

## Untuk persiapan sidang

| Dokumen | Isi | Prioritas |
|---|---|---|
| [EKSPERIMEN_SGO.md](EKSPERIMEN_SGO.md) | Metodologi SGO, hasil pengukuran nyata, pembuktian nilai hyperparameter, dan **temuan penting mengenai dataset** | **Baca lebih dulu** |
| [PENJELASAN_ML.md](PENJELASAN_ML.md) | Penjelasan sintaks & alur sistem machine learning langkah demi langkah — untuk menjelaskan kode saat sidang | **Tinggi** |
| [PANDUAN_DEMO.md](PANDUAN_DEMO.md) | Cara menjalankan sistem, akun, alur demonstrasi 7 langkah, jawaban untuk pertanyaan penguji | Tinggi |
| [../ml-engine/data/README.md](../ml-engine/data/README.md) | Asal-usul dataset, struktur kolom, peringatan mengenai kolom `Label` | Tinggi |
| [../arsip/README.md](../arsip/README.md) | Berkas lama yang menghasilkan angka tidak sah, beserta penggantinya | Tinggi |

## Perancangan sistem

| Dokumen | Isi |
|---|---|
| [perancangan-database.md](perancangan-database.md) | Rancangan tabel, kolom, dan relasi |
| [database_erd.md](database_erd.md) | Diagram hubungan antar entitas |
| [use-case-uml.md](use-case-uml.md) | Diagram use case |
| [aksi-dasar.md](aksi-dasar.md) | Rincian aksi dasar per use case |

## Referensi pengembangan

| Dokumen | Isi |
|---|---|
| [ALUR_SISTEM.md](ALUR_SISTEM.md) | Penelusuran alur sistem secara rinci |
| [WALKTHROUGH.md](WALKTHROUGH.md) | Panduan menyusuri kode |
| [CATATAN_PENGEMBANGAN.md](CATATAN_PENGEMBANGAN.md) | Catatan selama pengembangan |
| [README_LAMA_LENGKAP.md](README_LAMA_LENGKAP.md) | README versi panjang sebelum dirapikan; disimpan sebagai rujukan |

---

## Catatan mengenai keakuratan dokumen

Dokumen pada bagian **Referensi pengembangan** ditulis pada tahap awal, ketika
sistem masih memakai model tiruan dan angka yang ditulis tangan. Sebagian
isinya **sudah tidak lagi mencerminkan keadaan sistem sekarang** — terutama
bagian yang menyebut akurasi 82,45% / 93,27%.

Rujukan yang sahih untuk keadaan terkini adalah
[EKSPERIMEN_SGO.md](EKSPERIMEN_SGO.md) dan metadata model pada
`ml-engine/artifacts/model_metadata.json`.
