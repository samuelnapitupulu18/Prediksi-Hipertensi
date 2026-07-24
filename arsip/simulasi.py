import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import numpy as np

# ==========================================
# 1. MENYIAPKAN DATA DARI FILE CSV
# ==========================================
print("1. Membaca data dari CSV...")
file_path = r"C:\Users\ASUS\Downloads\dataset_gabungan_10000.csv"
df = pd.read_csv(file_path)

print(f"Total data yang dimuat: {len(df)} baris")

# Mengubah data teks menjadi angka (Label Encoding manual)
# XGBoost butuh angka, jadi Laki-laki = 1, Perempuan = 0
if df['Jenis_Kelamin'].dtype == object:
    df['Jenis_Kelamin'] = df['Jenis_Kelamin'].map({'Laki-laki': 1, 'Perempuan': 0})

# Memisahkan Fitur (X) dan Target/Kunci Jawaban (y)
# Kita membuang kolom 'Label' (karena itu jawabannya) dan 'Sumber' (tidak relevan untuk medis)
X = df.drop(['Label', 'Sumber'], axis=1)
y = df['Label']

# ==========================================
# 2. MEMBAGI DATA LATIH DAN UJI
# ==========================================
print("2. Membagi data menjadi 80% Latih (Training) dan 20% Uji (Testing)...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 3. MELATIH MODEL XGBOOST
# ==========================================
print("3. Membangun dan Melatih model XGBoost...")
jumlah_kelas = len(y.unique())
tipe_objektif = 'multi:softprob' if jumlah_kelas > 2 else 'binary:logistic'

model = xgb.XGBClassifier(
    learning_rate=0.035,
    max_depth=9,
    n_estimators=100,
    objective=tipe_objektif,
    num_class=jumlah_kelas if jumlah_kelas > 2 else None,
    eval_metric='logloss'
)
model.fit(X_train, y_train)

# ==========================================
# 4. PREDIKSI & EVALUASI
# ==========================================
print("4. Melakukan Prediksi pada data Uji...")
y_pred = model.predict(X_test)

print("5. Menghitung metrik evaluasi...")
accuracy = accuracy_score(y_test, y_pred)
print(f"\n====================================")
print(f"AKURASI MODEL XGBOOST: {accuracy * 100:.2f}%")
print(f"====================================\n")

print("Laporan Klasifikasi Detail:")
print(classification_report(y_test, y_pred))

# ==========================================
# 6. MELIHAT DATA YANG SESUAI DAN TIDAK SESUAI
# ==========================================
print("\n6. Menganalisis Prediksi (Sesuai vs Tidak Sesuai)...")
# Membuat dataframe khusus untuk hasil prediksi
df_hasil = X_test.copy()
df_hasil['Aktual (Kenyataan)'] = y_test.values
df_hasil['Prediksi XGBoost'] = y_pred

# Mencari tahu mana yang tebakannya benar dan mana yang salah
df_sesuai = df_hasil[df_hasil['Aktual (Kenyataan)'] == df_hasil['Prediksi XGBoost']]
df_tidak_sesuai = df_hasil[df_hasil['Aktual (Kenyataan)'] != df_hasil['Prediksi XGBoost']]

print(f"-> Prediksi Sesuai (Benar) : {len(df_sesuai)} pasien")
print(f"-> Prediksi Tidak Sesuai (Salah) : {len(df_tidak_sesuai)} pasien\n")

print("--- CONTOH 3 PASIEN YANG DIPREDIKSI SESUAI (BENAR) ---")
print(df_sesuai.head(3).to_string())

print("\n--- CONTOH 3 PASIEN YANG DIPREDIKSI TIDAK SESUAI (SALAH) ---")
print(df_tidak_sesuai.head(3).to_string())
print("\n")

# ==========================================
# 7. SIMULASI VISUALISASI MATPLOTLIB
# ==========================================
print("7. Membuka jendela visualisasi Matplotlib...")
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# --- Grafik 1 (Kiri Atas): Confusion Matrix ---
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
axes[0, 0].set_title(f'Confusion Matrix\n(Akurasi: {accuracy*100:.1f}%)', fontsize=14, pad=10)
axes[0, 0].set_ylabel('Kelas Aktual (Kenyataan)')
axes[0, 0].set_xlabel('Kelas Prediksi (Tebakan Model)')

# --- Grafik 2 (Kanan Atas): Feature Importance ---
nama_fitur = X.columns.tolist()
importances = model.feature_importances_
indices = np.argsort(importances)[::-1] 

axes[0, 1].bar(range(X.shape[1]), importances[indices], align="center", color='lightcoral')
axes[0, 1].set_xticks(range(X.shape[1]))
axes[0, 1].set_xticklabels([nama_fitur[i] for i in indices], rotation=45, ha='right')
axes[0, 1].set_title('Tingkat Kepentingan Fitur Terhadap Hipertensi', fontsize=14, pad=10)
axes[0, 1].set_ylabel('Skor Bobot XGBoost')

# --- Area 3 (Kiri Bawah): Ringkasan Teks Simulasi ---
axes[1, 0].axis('off') # Sembunyikan garis axis
info_text = (
    "RINGKASAN SIMULASI (TRAIN & TEST SPLIT)\n"
    "=========================================\n"
    f"Total Data      : {len(X)} Pasien\n"
    f"Data Latih (80%): {len(X_train)} Pasien (Untuk Belajar)\n"
    f"Data Uji   (20%): {len(X_test)} Pasien (Untuk Ujian/Tes)\n\n"
    "HASIL PREDIKSI (PADA DATA UJI)\n"
    "=========================================\n"
    f"Akurasi Keseluruhan          : {accuracy * 100:.2f}%\n"
    f"Tebakan Sesuai (Benar)       : {len(df_sesuai)} Pasien\n"
    f"Tebakan Tidak Sesuai (Salah) : {len(df_tidak_sesuai)} Pasien"
)
axes[1, 0].text(0.1, 0.5, info_text, fontsize=13, va='center', ha='left', family='monospace', 
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray', boxstyle='round,pad=1'))

# --- Area 4 (Kanan Bawah): Tabel Contoh Prediksi ---
axes[1, 1].axis('off')
# Ambil contoh 2 yang benar, dan 2 yang salah (jika ada)
sample_benar = df_sesuai.head(2).copy()
sample_benar['Status'] = 'SESUAI (BENAR)'

sample_salah = df_tidak_sesuai.head(2).copy()
if not sample_salah.empty:
    sample_salah['Status'] = 'TIDAK SESUAI (SALAH)'
    df_sample = pd.concat([sample_benar, sample_salah])
else:
    df_sample = sample_benar

# Tampilkan kolom inti saja agar muat di layar
kolom_tampil = ['Usia', 'TDS', 'TDD', 'IMT', 'Aktual (Kenyataan)', 'Prediksi XGBoost', 'Status']
df_table = df_sample[kolom_tampil]

# Membuat tabel di Matplotlib
table = axes[1, 1].table(cellText=df_table.values, colLabels=df_table.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2) # Melebarkan baris tabel
axes[1, 1].set_title('Contoh Detail Prediksi Pasien (Sesuai vs Tidak Sesuai)', fontsize=14, pad=10)

plt.tight_layout()
plt.show()
