<template>
  <div class="space-y-6 max-w-6xl mx-auto pb-12">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white">
        Uji Prediksi Live — Pembuktian Nilai Hyperparameter
      </h1>
      <p class="mt-1 text-sm text-slate-500 dark:text-slate-400 max-w-3xl">
        Menjawab satu pertanyaan: apakah nilai
        <span class="font-mono font-bold text-slate-700 dark:text-slate-300">learning_rate 0.035</span>,
        <span class="font-mono font-bold text-slate-700 dark:text-slate-300">max_depth 9</span>,
        <span class="font-mono font-bold text-slate-700 dark:text-slate-300">n_estimators 285</span>
        yang dipaparkan pada laporan benar-benar dihasilkan oleh Social Group Optimization?
        Tentukan jumlah iterasi sesuka Anda, lalu jalankan.
      </p>
    </div>

    <!-- ══════════ UJI A: waktu eksekusi pada jumlah iterasi yang sama ══════════ -->
    <div class="rounded-2xl bg-white dark:bg-slate-900 p-6 ring-1 ring-slate-200 dark:ring-slate-800">
      <div class="flex items-start justify-between gap-4 mb-4">
        <div>
          <h2 class="text-base font-bold text-slate-900 dark:text-white">
            Uji A — Akurasi &amp; Waktu Eksekusi pada Jumlah Iterasi Tertentu
          </h2>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-3xl">
            Tentukan jumlah iterasi boosting untuk masing-masing model. Bila keduanya
            disamakan, selisih waktu yang terukur murni berasal dari perbedaan
            <span class="font-mono">learning_rate</span> dan <span class="font-mono">max_depth</span>,
            bukan dari banyaknya pohon.
          </p>
        </div>
        <span class="shrink-0 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">
          cepat, ± 1 detik
        </span>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-blue-600 dark:text-blue-400">Iterasi — Default</label>
          <input v-model.number="timingConfig.default_iterations" type="number" min="1" max="2000" :class="inputClass" />
          <p class="text-[10px] text-slate-400">n_estimators</p>
        </div>
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-emerald-600 dark:text-emerald-400">Iterasi — Optimasi</label>
          <input v-model.number="timingConfig.optimized_iterations" type="number" min="1" max="2000" :class="inputClass" />
          <p class="text-[10px] text-slate-400">n_estimators</p>
        </div>
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-400">Pengulangan</label>
          <input v-model.number="timingConfig.repeats" type="number" min="1" max="10" :class="inputClass" />
          <p class="text-[10px] text-slate-400">diambil median</p>
        </div>
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-400">Seed</label>
          <input v-model.number="timingConfig.seed" type="number" min="0" max="9999" :class="inputClass" />
        </div>
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-400">Status</label>
          <div
            class="rounded-xl px-3 py-2.5 text-xs font-bold"
            :class="iterasiSama
              ? 'bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300'
              : 'bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300'"
          >
            {{ iterasiSama ? 'Iterasi sama' : 'Iterasi berbeda' }}
          </div>
          <button
            v-if="!iterasiSama"
            @click="timingConfig.optimized_iterations = timingConfig.default_iterations"
            class="text-[10px] font-bold text-blue-600 dark:text-blue-400 hover:underline"
          >Samakan</button>
        </div>
      </div>

      <div class="mt-5 flex flex-wrap items-center gap-4">
        <button
          @click="runTiming"
          :disabled="timingLoading"
          class="px-6 py-2.5 text-sm font-bold text-white bg-slate-800 dark:bg-slate-700 rounded-xl shadow disabled:opacity-60 transition-all active:scale-95 flex items-center gap-2"
        >
          <svg v-if="timingLoading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ timingLoading ? 'Mengukur…' : 'Ukur Akurasi & Waktu' }}
        </button>
      </div>

      <div v-if="timingError" class="mt-4 p-4 rounded-xl border border-red-200 dark:border-red-800/50 bg-red-50 dark:bg-red-950/30">
        <p class="text-sm font-medium text-red-700 dark:text-red-300">{{ timingError }}</p>
      </div>

      <!-- Hasil Uji A -->
      <div v-if="timing" class="mt-6 space-y-4">
        <div class="overflow-x-auto rounded-xl ring-1 ring-slate-200 dark:ring-slate-800">
          <table class="w-full text-sm">
            <thead class="bg-slate-50 dark:bg-slate-800/50">
              <tr>
                <th class="px-5 py-3 text-left text-xs font-bold text-slate-500 dark:text-slate-400">Model</th>
                <th class="px-3 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">lr</th>
                <th class="px-3 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">depth</th>
                <th class="px-3 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Iterasi</th>
                <th class="px-3 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Accuracy</th>
                <th class="px-3 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Macro F1</th>
                <th class="px-3 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Waktu Latih</th>
                <th class="px-5 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Per Pohon</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="m in timing.models" :key="m.key"
                  :class="m.key === 'optimized' ? 'bg-emerald-50/40 dark:bg-emerald-900/10' : ''">
                <td class="px-5 py-3 font-bold text-slate-800 dark:text-slate-200">{{ m.label }}</td>
                <td class="px-3 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ m.hyperparameters.learning_rate }}</td>
                <td class="px-3 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ m.hyperparameters.max_depth }}</td>
                <td class="px-3 py-3 text-right font-mono font-bold text-slate-800 dark:text-slate-200">{{ m.hyperparameters.n_estimators }}</td>
                <td class="px-3 py-3 text-right font-mono font-bold text-slate-800 dark:text-slate-200">{{ m.metrics.accuracy }}%</td>
                <td class="px-3 py-3 text-right font-mono font-bold text-slate-800 dark:text-slate-200">{{ m.metrics.f1 }}%</td>
                <td class="px-3 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ m.timing.training_median_s }} s</td>
                <td class="px-5 py-3 text-right font-mono text-slate-500 dark:text-slate-400">{{ m.timing.training_per_tree_ms }} ms</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div class="rounded-xl bg-slate-50 dark:bg-slate-800/50 p-4">
            <p class="text-[11px] font-bold text-slate-500 dark:text-slate-400">Selisih Accuracy</p>
            <p class="mt-1 text-xl font-extrabold"
               :class="timing.comparison.accuracy_diff >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'">
              {{ timing.comparison.accuracy_diff >= 0 ? '+' : '' }}{{ timing.comparison.accuracy_diff }}%
            </p>
          </div>
          <div class="rounded-xl bg-slate-50 dark:bg-slate-800/50 p-4">
            <p class="text-[11px] font-bold text-slate-500 dark:text-slate-400">Selisih Macro F1</p>
            <p class="mt-1 text-xl font-extrabold"
               :class="timing.comparison.f1_diff >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'">
              {{ timing.comparison.f1_diff >= 0 ? '+' : '' }}{{ timing.comparison.f1_diff }}%
            </p>
          </div>
          <div class="rounded-xl bg-slate-50 dark:bg-slate-800/50 p-4">
            <p class="text-[11px] font-bold text-slate-500 dark:text-slate-400">Selisih Waktu</p>
            <p class="mt-1 text-xl font-extrabold text-amber-600 dark:text-amber-400">
              {{ timing.comparison.training_diff_s >= 0 ? '+' : '' }}{{ timing.comparison.training_diff_s }} s
            </p>
            <p class="text-[10px] text-slate-400 mt-0.5">rasio {{ timing.comparison.training_ratio }}×</p>
          </div>
          <div class="rounded-xl bg-slate-50 dark:bg-slate-800/50 p-4">
            <p class="text-[11px] font-bold text-slate-500 dark:text-slate-400">Lebih Cepat</p>
            <p class="mt-1 text-sm font-extrabold text-slate-800 dark:text-slate-200 leading-tight">
              {{ timing.comparison.faster_model }}
            </p>
          </div>
        </div>

        <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
          Waktu latih adalah <strong>median dari {{ timing.config.repeats }} kali pelatihan</strong>
          (rentang {{ timing.models[0].timing.training_min_s }}–{{ timing.models[0].timing.training_max_s }} s
          untuk model default), agar tidak terganggu beban lain pada komputer.
          Yang dimaksud "iterasi" di sini adalah {{ timing.config.iteration_meaning }}.
        </p>
      </div>
    </div>

    <!-- ══════════ UJI B: pembuktian nilai hyperparameter ══════════ -->
    <div class="rounded-2xl bg-white dark:bg-slate-900 p-6 ring-1 ring-slate-200 dark:ring-slate-800">
      <h2 class="text-base font-bold text-slate-900 dark:text-white mb-1">
        Uji B — Pembuktian Nilai Hyperparameter lewat SGO
      </h2>
      <p class="text-xs text-slate-500 dark:text-slate-400 mb-4 max-w-3xl">
        Menjalankan pencarian SGO yang sesungguhnya untuk memeriksa apakah nilai
        0.035 / 9 / 285 dapat direproduksi. Di sini "iterasi" berarti generasi pencarian SGO.
      </p>
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-400">Iterasi SGO</label>
          <input v-model.number="config.iterations" type="number" min="1" max="500" :class="inputClass" />
        </div>
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-400">Populasi</label>
          <input v-model.number="config.population_size" type="number" min="3" max="50" :class="inputClass" />
        </div>
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-400">Seed</label>
          <input v-model.number="config.seed" type="number" min="0" max="9999" :class="inputClass" />
        </div>
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-400">Pengulangan</label>
          <input v-model.number="config.verification_runs" type="number" min="1" max="10" :class="inputClass" />
          <p class="text-[10px] text-slate-400">seed berbeda</p>
        </div>
        <div class="space-y-1.5">
          <label class="block text-xs font-bold text-slate-600 dark:text-slate-400">Perkiraan</label>
          <div
            class="rounded-xl px-3 py-2.5 text-sm font-mono font-bold"
            :class="estimatedSeconds > 900
              ? 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300'
              : estimatedSeconds > 180
                ? 'bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300'
                : 'bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300'"
          >
            ≈ {{ estimatedLabel }}
          </div>
          <p v-if="estimatedSeconds > 900" class="text-[10px] text-red-500">
            Melebihi batas 30 menit — kurangi nilainya
          </p>
        </div>
      </div>

      <div class="mt-4 flex items-center gap-3">
        <label class="inline-flex items-center gap-2 cursor-pointer">
          <input type="checkbox" v-model="config.include_blood_pressure" class="w-4 h-4 accent-amber-600 rounded" />
          <span class="text-xs font-medium text-slate-600 dark:text-slate-400">
            Sertakan tekanan darah sebagai fitur
            <span class="text-slate-400">(membuat akurasi kedua model 100% — lihat catatan)</span>
          </span>
        </label>
      </div>

      <div class="mt-5 flex flex-wrap items-center gap-4">
        <button
          @click="runComparison"
          :disabled="loading"
          class="px-7 py-3 text-sm font-bold text-white bg-gradient-to-r from-indigo-600 to-blue-600 rounded-xl shadow-lg shadow-indigo-500/30 disabled:opacity-60 transition-all active:scale-95 flex items-center gap-2"
        >
          <svg v-if="loading" class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ loading ? 'Menjalankan optimasi…' : 'Jalankan Pembuktian' }}
        </button>
        <p v-if="loading" class="text-xs text-slate-500 dark:text-slate-400">
          Melatih model sungguhan. Mohon tunggu, jangan tutup halaman.
        </p>
      </div>

      <div v-if="error" class="mt-4 p-4 rounded-xl border border-red-200 dark:border-red-800/50 bg-red-50 dark:bg-red-950/30">
        <p class="text-sm font-medium text-red-700 dark:text-red-300">{{ error }}</p>
      </div>
    </div>

    <template v-if="result">
      <!-- VERDIKT -->
      <div
        class="rounded-2xl p-6 ring-1"
        :class="verdictStyle.box"
      >
        <div class="flex items-start gap-4">
          <div class="h-11 w-11 rounded-xl flex items-center justify-center shrink-0" :class="verdictStyle.badge">
            <span class="text-xl font-black">{{ verdictStyle.icon }}</span>
          </div>
          <div>
            <p class="text-xs font-bold uppercase tracking-wide" :class="verdictStyle.label">Hasil Pembuktian</p>
            <h2 class="text-xl font-extrabold mt-0.5" :class="verdictStyle.title">
              {{ verdictStyle.heading }}
            </h2>
            <p class="mt-2 text-sm leading-relaxed" :class="verdictStyle.text">
              {{ result.verification.summary }}
            </p>
          </div>
        </div>
      </div>

      <!-- Perbandingan tiga nilai -->
      <div class="rounded-2xl bg-white dark:bg-slate-900 ring-1 ring-slate-200 dark:ring-slate-800 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800">
          <h2 class="text-sm font-bold text-slate-900 dark:text-white">Nilai yang Dipaparkan vs Temuan SGO</h2>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Toleransi = 10% dari lebar rentang pencarian tiap parameter
          </p>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-50 dark:bg-slate-800/50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-bold text-slate-500 dark:text-slate-400">Parameter</th>
                <th class="px-6 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Rentang Cari</th>
                <th class="px-6 py-3 text-right text-xs font-bold text-amber-600 dark:text-amber-400">Dipaparkan</th>
                <th class="px-6 py-3 text-right text-xs font-bold text-emerald-600 dark:text-emerald-400">Ditemukan SGO</th>
                <th class="px-6 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Selisih</th>
                <th class="px-6 py-3 text-center text-xs font-bold text-slate-500 dark:text-slate-400">Status</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="p in result.verification.parameters" :key="p.parameter">
                <td class="px-6 py-3 font-mono text-xs text-slate-700 dark:text-slate-300">{{ p.parameter }}</td>
                <td class="px-6 py-3 text-right font-mono text-xs text-slate-400">
                  {{ p.search_range[0] }} – {{ p.search_range[1] }}
                </td>
                <td class="px-6 py-3 text-right font-mono font-bold text-amber-700 dark:text-amber-400">{{ p.claimed }}</td>
                <td class="px-6 py-3 text-right font-mono font-bold text-emerald-700 dark:text-emerald-400">{{ p.found }}</td>
                <td class="px-6 py-3 text-right font-mono text-slate-600 dark:text-slate-400">{{ p.difference }}</td>
                <td class="px-6 py-3 text-center">
                  <span
                    class="inline-block px-2.5 py-1 rounded-lg text-[11px] font-bold"
                    :class="p.match
                      ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'
                      : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'"
                  >{{ p.match ? 'COCOK' : 'TIDAK COCOK' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tiga model -->
      <div class="rounded-2xl bg-white dark:bg-slate-900 ring-1 ring-slate-200 dark:ring-slate-800 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800">
          <h2 class="text-sm font-bold text-slate-900 dark:text-white">Performa Ketiga Model (Data Uji)</h2>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Akurasi bila asal menebak kelas terbanyak: {{ result.dataset.majority_baseline }}%
          </p>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-50 dark:bg-slate-800/50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-bold text-slate-500 dark:text-slate-400">Model</th>
                <th class="px-4 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">learning_rate</th>
                <th class="px-4 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">max_depth</th>
                <th class="px-4 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">n_estimators</th>
                <th class="px-4 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Accuracy</th>
                <th class="px-4 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Macro F1</th>
                <th class="px-6 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">Waktu Latih</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="m in modelRows" :key="m.key" :class="m.key === 'sgo' ? 'bg-emerald-50/40 dark:bg-emerald-900/10' : ''">
                <td class="px-6 py-3 font-bold text-slate-800 dark:text-slate-200">{{ m.label }}</td>
                <td class="px-4 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ m.lr }}</td>
                <td class="px-4 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ m.depth }}</td>
                <td class="px-4 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ m.trees }}</td>
                <td class="px-4 py-3 text-right font-mono font-bold text-slate-800 dark:text-slate-200">{{ m.acc }}%</td>
                <td class="px-4 py-3 text-right font-mono font-bold text-slate-800 dark:text-slate-200">{{ m.f1 }}%</td>
                <td class="px-6 py-3 text-right font-mono text-slate-500 dark:text-slate-400">{{ m.time }} s</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="px-6 py-3 bg-slate-50 dark:bg-slate-800/40 border-t border-slate-100 dark:border-slate-800 space-y-1.5">
          <p class="text-xs text-slate-500 dark:text-slate-400">
            <strong class="text-slate-700 dark:text-slate-300">Baris "XGBoost Default"</strong> memakai
            nilai bawaan pustaka — bukan pilihan peneliti —
            <span class="font-mono">{{ result.default.source }}</span>.
            Jalankan <span class="font-mono">scripts/show_xgboost_defaults.py</span> untuk membuktikannya.
          </p>
          <p class="text-xs text-slate-500 dark:text-slate-400">
            Waktu optimasi SGO: <strong class="font-mono">{{ result.sgo.timing.optimization_s }} s</strong>
            untuk {{ result.config.total_model_trainings }} pelatihan model —
            biaya tambahan <strong class="font-mono">+{{ result.improvement.extra_time_s }} s</strong>
            dibanding melatih model default saja.
          </p>
        </div>
      </div>

      <!-- Reproduksibilitas -->
      <div v-if="result.reproducibility.length > 1" class="rounded-2xl bg-white dark:bg-slate-900 ring-1 ring-slate-200 dark:ring-slate-800 overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800">
          <h2 class="text-sm font-bold text-slate-900 dark:text-white">Uji Konsistensi Antar Seed</h2>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Optimasi diulang dengan seed berbeda. Bila nilainya berpindah-pindah,
            berarti tidak ada satu titik optimum tunggal yang bisa diklaim.
          </p>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-slate-50 dark:bg-slate-800/50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-bold text-slate-500 dark:text-slate-400">Seed</th>
                <th class="px-4 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">learning_rate</th>
                <th class="px-4 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">max_depth</th>
                <th class="px-4 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">n_estimators</th>
                <th class="px-6 py-3 text-right text-xs font-bold text-slate-500 dark:text-slate-400">F1 Validasi</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
              <tr v-for="r in result.reproducibility" :key="r.seed">
                <td class="px-6 py-3 font-mono text-slate-700 dark:text-slate-300">{{ r.seed }}</td>
                <td class="px-4 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ r.learning_rate }}</td>
                <td class="px-4 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ r.max_depth }}</td>
                <td class="px-4 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ r.n_estimators }}</td>
                <td class="px-6 py-3 text-right font-mono text-slate-700 dark:text-slate-300">{{ r.validation_f1 }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Konvergensi -->
      <div class="rounded-2xl bg-white dark:bg-slate-900 p-6 ring-1 ring-slate-200 dark:ring-slate-800">
        <h2 class="text-sm font-bold text-slate-900 dark:text-white">Konvergensi SGO per Iterasi</h2>
        <p class="text-xs text-slate-500 dark:text-slate-400 mb-4">
          Fitness ({{ result.sgo.fitness_metric }}) — menunjukkan pengaruh jumlah iterasi
        </p>
        <v-chart class="h-64 w-full" :option="convergenceOption" autoresize />
      </div>

      <!-- Catatan -->
      <div class="rounded-2xl bg-slate-50 dark:bg-slate-800/50 p-5 ring-1 ring-slate-200 dark:ring-slate-700">
        <p class="text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Catatan</p>
        <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{{ result.dataset.feature_set_note }}</p>
        <p class="mt-2 text-xs text-slate-500 dark:text-slate-400">
          Dataset <span class="font-mono">{{ result.dataset.path }}</span> —
          {{ result.dataset.total_samples.toLocaleString('id-ID') }} sampel,
          {{ result.dataset.n_features }} fitur, 2 kelas.
          Pembagian {{ result.dataset.split.train }} latih /
          {{ result.dataset.split.validation }} validasi /
          {{ result.dataset.split.test }} uji.
          Hanya tiga parameter yang dioptimasi: {{ result.config.tuned_parameters.join(', ') }}.
        </p>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { TooltipComponent, GridComponent, LegendComponent } from 'echarts/components'
import VChart from 'vue-echarts'
import { optimizationService } from '../../services/optimizationService'

use([CanvasRenderer, LineChart, TooltipComponent, GridComponent, LegendComponent])

const inputClass =
  'w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-3 py-2.5 text-sm font-mono dark:text-white outline-none focus:ring-2 focus:ring-blue-500'

const config = reactive({
  iterations: 8,
  population_size: 5,
  seed: 42,
  verification_runs: 3,
  include_blood_pressure: false,
})

const loading = ref(false)
const error = ref('')
const result = ref<any>(null)

// ---------------------------------------------------------------- Uji A
// Perbandingan akurasi & waktu pada jumlah iterasi boosting (n_estimators)
// yang ditentukan sendiri untuk masing-masing model.
const timingConfig = reactive({
  default_iterations: 100,
  optimized_iterations: 100,
  repeats: 3,
  seed: 42,
  include_blood_pressure: false,
})

const timingLoading = ref(false)
const timingError = ref('')
const timing = ref<any>(null)

const iterasiSama = computed(
  () => timingConfig.default_iterations === timingConfig.optimized_iterations
)

const runTiming = async () => {
  timingLoading.value = true
  timingError.value = ''
  try {
    timing.value = await optimizationService.timing({
      ...timingConfig,
      include_blood_pressure: config.include_blood_pressure,
    })
  } catch (e: any) {
    timingError.value =
      e?.response?.data?.message ||
      'Gagal menjalankan uji waktu. Pastikan ML Engine sedang berjalan.'
  } finally {
    timingLoading.value = false
  }
}

// Tiap generasi menjalankan dua fase yang masing-masing mengevaluasi seluruh
// populasi, ditambah evaluasi populasi awal — dikali jumlah pengulangan seed.
const estimatedSeconds = computed(() => {
  const perRun = config.population_size + config.iterations * config.population_size * 2
  return Math.max(1, Math.round(perRun * config.verification_runs * 0.15))
})

const estimatedLabel = computed(() => {
  const s = estimatedSeconds.value
  if (s < 60) return `${s} s`
  const m = Math.floor(s / 60)
  return s % 60 === 0 ? `${m} mnt` : `${m} mnt ${s % 60} s`
})

const modelRows = computed(() => {
  if (!result.value) return []
  return (['default', 'claimed', 'sgo'] as const).map((key) => {
    const m = result.value[key]
    return {
      key,
      label: m.label,
      lr: m.hyperparameters.learning_rate,
      depth: m.hyperparameters.max_depth,
      trees: m.hyperparameters.n_estimators,
      acc: m.metrics.accuracy,
      f1: m.metrics.f1,
      time: m.timing.training_s,
    }
  })
})

const verdictStyle = computed(() => {
  const v = result.value?.verification?.verdict
  if (v === 'cocok') {
    return {
      icon: '✓',
      heading: 'Nilai yang dipaparkan TERBUKTI',
      box: 'bg-emerald-50 dark:bg-emerald-900/20 ring-emerald-200 dark:ring-emerald-800/50',
      badge: 'bg-emerald-600 text-white',
      label: 'text-emerald-700 dark:text-emerald-400',
      title: 'text-emerald-800 dark:text-emerald-300',
      text: 'text-emerald-700 dark:text-emerald-400',
    }
  }
  if (v === 'sebagian') {
    return {
      icon: '!',
      heading: 'Terbukti sebagian',
      box: 'bg-amber-50 dark:bg-amber-900/20 ring-amber-200 dark:ring-amber-800/50',
      badge: 'bg-amber-500 text-white',
      label: 'text-amber-700 dark:text-amber-400',
      title: 'text-amber-800 dark:text-amber-300',
      text: 'text-amber-700 dark:text-amber-400',
    }
  }
  return {
    icon: '✕',
    heading: 'Nilai yang dipaparkan TIDAK terbukti',
    box: 'bg-red-50 dark:bg-red-900/20 ring-red-200 dark:ring-red-800/50',
    badge: 'bg-red-600 text-white',
    label: 'text-red-700 dark:text-red-400',
    title: 'text-red-800 dark:text-red-300',
    text: 'text-red-700 dark:text-red-400',
  }
})

const convergenceOption = computed(() => {
  const conv = result.value?.convergence ?? []
  return {
    tooltip: { trigger: 'axis' },
    legend: {
      data: ['Fitness Terbaik', 'Rata-rata Populasi'],
      bottom: 0,
      textStyle: { color: '#94a3b8' },
    },
    grid: { left: 60, right: 24, top: 20, bottom: 45 },
    xAxis: {
      type: 'category',
      name: 'Iterasi',
      data: conv.map((c: any) => c.iteration),
      axisLabel: { color: '#94a3b8' },
    },
    yAxis: {
      type: 'value',
      name: 'Macro F1 (%)',
      scale: true,
      axisLabel: { color: '#94a3b8', formatter: '{value}%' },
    },
    series: [
      {
        name: 'Fitness Terbaik',
        type: 'line',
        smooth: true,
        symbolSize: 8,
        data: conv.map((c: any) => c.best_fitness),
        itemStyle: { color: '#10b981' },
        lineStyle: { width: 3 },
      },
      {
        name: 'Rata-rata Populasi',
        type: 'line',
        smooth: true,
        symbolSize: 6,
        data: conv.map((c: any) => c.mean_fitness),
        itemStyle: { color: '#6366f1' },
        lineStyle: { width: 2, type: 'dashed' },
      },
    ],
  }
})

const runComparison = async () => {
  loading.value = true
  error.value = ''
  try {
    result.value = await optimizationService.compare({ ...config })
  } catch (e: any) {
    error.value =
      e?.response?.data?.message ||
      'Gagal menjalankan pembuktian. Pastikan ML Engine sedang berjalan.'
  } finally {
    loading.value = false
  }
}
</script>
