import api from './api'

// =====================================================================
// Optimization Service — menjalankan perbandingan XGBoost Default vs
// XGBoost + SGO pada ML Engine melalui backend Laravel.
//
// Seluruh angka yang dikembalikan dihitung saat permintaan diproses
// (pelatihan model sungguhan). Tidak ada nilai yang disiapkan di muka.
// =====================================================================

export interface OptimizationConfig {
  iterations: number
  population_size: number
  seed?: number
  include_blood_pressure?: boolean
  /** Berapa kali optimasi diulang dengan seed berbeda untuk menguji konsistensi. */
  verification_runs?: number
}

export interface TimingConfig {
  /** Jumlah iterasi boosting (n_estimators) untuk model default. */
  default_iterations: number
  /** Jumlah iterasi boosting (n_estimators) untuk model hasil optimasi. */
  optimized_iterations: number
  seed?: number
  /** Pengulangan pengukuran waktu; hasilnya diambil median. */
  repeats?: number
  include_blood_pressure?: boolean
}

export const optimizationService = {
  /**
   * Metadata model produksi: metrik pada data uji, hyperparameter hasil SGO,
   * dan kepentingan fitur — seluruhnya dihitung saat pelatihan.
   */
  modelInfo: async () => {
    const res = await api.get('/optimization/model-info')
    return res.data.data
  },

  /**
   * Uji akurasi & waktu eksekusi kedua model pada jumlah iterasi boosting
   * yang ditentukan sendiri. Ringan — hanya melatih dua model.
   */
  timing: async (config: TimingConfig) => {
    const res = await api.post('/optimization/timing', config, { timeout: 300000 })
    return res.data.data
  },

  compare: async (config: OptimizationConfig) => {
    // Proses melatih ratusan hingga ribuan model, jadi batas waktu dilonggarkan
    // menjadi 30 menit — sejalan dengan ML_ENGINE_OPTIMIZE_TIMEOUT di backend.
    const res = await api.post('/optimization/compare', config, { timeout: 1800000 })
    return res.data.data
  },
}
