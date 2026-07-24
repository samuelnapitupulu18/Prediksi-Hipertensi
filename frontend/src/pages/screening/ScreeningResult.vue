<template>
  <div>
    <!-- Error State -->
    <div v-if="loadError" class="flex flex-col items-center justify-center py-20 gap-4 max-w-md mx-auto text-center">
      <div class="h-16 w-16 rounded-2xl bg-red-100 dark:bg-red-900/30 flex items-center justify-center text-3xl">⚠️</div>
      <p class="text-sm font-medium text-slate-700 dark:text-slate-300">{{ loadError }}</p>
      <div class="flex items-center gap-3">
        <button @click="fetchScreening" class="px-5 py-2.5 text-sm font-bold text-white bg-blue-600 rounded-xl hover:bg-blue-700 transition-all active:scale-95">Coba Lagi</button>
        <router-link :to="{ name: 'screening-new' }" class="px-5 py-2.5 text-sm font-bold text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-700 transition-all active:scale-95">Skrining Baru</router-link>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="!screening" class="flex flex-col items-center justify-center py-20 gap-4">
      <div class="relative">
        <div class="h-16 w-16 rounded-full border-4 border-slate-200 dark:border-slate-700"></div>
        <div class="absolute top-0 left-0 h-16 w-16 rounded-full border-4 border-blue-500 border-t-transparent animate-spin"></div>
      </div>
      <p class="text-sm font-medium text-slate-500 dark:text-slate-400">Memuat hasil skrining...</p>
    </div>

    <!-- Main Content -->
    <div v-else class="space-y-6 max-w-4xl mx-auto pb-12">

    <!-- Top Action Bar -->
    <div class="flex items-center justify-between sticky top-0 z-20 bg-slate-50 dark:bg-slate-950 py-3 -mx-2 px-2 sm:mx-0 sm:px-0">
      <div class="flex items-center gap-3">
        <button @click="router.back()" class="p-2.5 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all active:scale-95 shadow-sm">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-slate-600 dark:text-slate-300"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <div>
          <h1 class="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">Laporan Hasil Skrining</h1>
          <p class="text-xs text-slate-500 dark:text-slate-400">{{ formatDate(screening.created_at) }}</p>
        </div>
      </div>
      <button @click="downloadPDF" :disabled="downloading" class="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white px-4 py-2.5 rounded-xl text-sm font-bold transition-all flex items-center gap-2 shadow-lg shadow-indigo-500/20 active:scale-95 disabled:opacity-60">
        <svg v-if="downloading" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
        <span class="hidden sm:inline">{{ downloading ? 'Memproses...' : 'Unduh PDF' }}</span>
      </button>
    </div>

    <!-- ═══ PDF CONTENT START ═══ -->
    <div id="pdf-content" class="space-y-6">

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- SECTION A: HEADER & EXECUTIVE SUMMARY                            -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 overflow-hidden shadow-xl shadow-slate-200/30 dark:shadow-slate-900/30">
        
        <!-- Risk Level Hero Banner -->
        <div :class="[getRiskBannerClass(conclusion?.bpClassification?.category)]" class="p-6 sm:p-8 relative overflow-hidden">
          <!-- Background pattern -->
          <div class="absolute inset-0 opacity-10">
            <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="pulse" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="1.5" fill="currentColor"/></pattern></defs><rect width="100%" height="100%" fill="url(#pulse)"/></svg>
          </div>
          
          <div class="relative z-10 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <p class="text-sm font-bold uppercase tracking-widest opacity-80 mb-1">Hasil Skrining Akhir</p>
              <h2 class="text-2xl sm:text-3xl font-black tracking-tight">
                {{ ['elevated', 'stage1', 'stage2', 'crisis'].includes(conclusion?.bpClassification?.category || '') ? 'Berisiko Hipertensi' : 'Tidak Berisiko Hipertensi' }}
              </h2>
              <p class="text-sm font-medium opacity-90 mt-1">Berdasarkan Pedoman Klinis PERKI & AI</p>
            </div>
            <!-- Confidence Circle -->
            <div class="relative h-20 w-20 sm:h-24 sm:w-24 flex-shrink-0">
              <svg class="h-full w-full -rotate-90" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="42" stroke="currentColor" stroke-width="8" fill="none" class="opacity-20"/>
                <circle cx="50" cy="50" r="42" stroke="currentColor" stroke-width="8" fill="none" stroke-linecap="round"
                  :stroke-dasharray="`${(prediction?.confidence_score || 0) * 264} 264`"
                  class="transition-all duration-1000 ease-out"/>
              </svg>
              <div class="absolute inset-0 flex flex-col items-center justify-center">
                <span class="text-xl sm:text-2xl font-black">{{ ((prediction?.confidence_score || 0) * 100).toFixed(0) }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Patient Info Strip -->
        <div class="bg-white dark:bg-slate-900 p-5 sm:p-6 border-t border-slate-200/60 dark:border-slate-800/60">
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 text-sm">
            <div>
              <p class="text-slate-400 dark:text-slate-500 font-medium text-xs uppercase tracking-wide">Pasien</p>
              <p class="font-bold text-slate-900 dark:text-white mt-0.5">{{ screening.patient?.name || screening.name || '-' }}</p>
            </div>
            <div>
              <p class="text-slate-400 dark:text-slate-500 font-medium text-xs uppercase tracking-wide">NIK</p>
              <p class="font-bold text-slate-900 dark:text-white mt-0.5 font-mono text-xs">{{ screening.patient?.nik || screening.nik || '-' }}</p>
            </div>
            <div>
              <p class="text-slate-400 dark:text-slate-500 font-medium text-xs uppercase tracking-wide">Usia / JK</p>
              <p class="font-bold text-slate-900 dark:text-white mt-0.5">{{ screening.age }} thn / {{ screening.gender === 'male' ? 'L' : 'P' }}</p>
            </div>
            <div>
              <p class="text-slate-400 dark:text-slate-500 font-medium text-xs uppercase tracking-wide">Tekanan Darah</p>
              <p class="font-bold text-slate-900 dark:text-white mt-0.5 font-mono">{{ screening.systolic_bp }}/{{ screening.diastolic_bp }} <span class="text-slate-400 font-normal">mmHg</span></p>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- SECTION B: KESIMPULAN KLINIS (CLINICAL SUMMARY)                   -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div v-if="conclusion" class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20">
        <div class="flex items-center gap-3 mb-5">
          <div class="h-10 w-10 rounded-xl bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 flex items-center justify-center text-lg">📋</div>
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Kesimpulan Klinis</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Ringkasan interpretasi berdasarkan data skrining</p>
          </div>
        </div>
        
        <!-- Summary box -->
        <div :class="[getRiskSummaryClass(conclusion?.bpClassification?.category)]" class="p-5 rounded-xl border mb-6">
          <p class="text-sm font-medium leading-relaxed">{{ conclusion.summary }}</p>
        </div>

        <!-- BP & BMI Classification side by side -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- BP Classification -->
          <div :class="[conclusion.bpClassification.bgColor, conclusion.bpClassification.darkBgColor, conclusion.bpClassification.borderColor, conclusion.bpClassification.darkBorderColor]" class="p-4 rounded-xl border">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Tekanan Darah</span>
              <span :class="[conclusion.bpClassification.color]" class="text-xs font-black uppercase tracking-wider">{{ conclusion.bpClassification.label }}</span>
            </div>
            <p class="text-2xl font-black text-slate-900 dark:text-white font-mono">{{ screening.systolic_bp }}<span class="text-slate-400 text-lg">/</span>{{ screening.diastolic_bp }} <span class="text-sm font-medium text-slate-400">mmHg</span></p>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 leading-relaxed">Standar: Pedoman PERKI (Indonesia)</p>
          </div>

          <!-- BMI Classification -->
          <div :class="[conclusion.bmiClassification.bgColor, conclusion.bmiClassification.darkBgColor, conclusion.bmiClassification.borderColor, conclusion.bmiClassification.darkBorderColor]" class="p-4 rounded-xl border">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">IMT (BMI)</span>
              <span :class="[conclusion.bmiClassification.color]" class="text-xs font-black uppercase tracking-wider">{{ conclusion.bmiClassification.label }}</span>
            </div>
            <p class="text-2xl font-black text-slate-900 dark:text-white font-mono">{{ screening.bmi?.toFixed?.(1) || screening.bmi }} <span class="text-sm font-medium text-slate-400">kg/m²</span></p>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 leading-relaxed">Standar: WHO Asia-Pacific ({{ conclusion.bmiClassification.range }})</p>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- SECTION C: PENJELASAN KLINIS HIPERTENSI                          -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div v-if="conclusion" class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20">
        <div class="flex items-center gap-3 mb-5">
          <div class="h-10 w-10 rounded-xl bg-purple-100 dark:bg-purple-500/20 text-purple-600 dark:text-purple-400 flex items-center justify-center text-lg">🩺</div>
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Penjelasan Klinis</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Informasi medis mengenai kondisi hipertensi pasien</p>
          </div>
        </div>

        <div class="prose prose-sm dark:prose-invert max-w-none">
          <div class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed whitespace-pre-line">{{ conclusion.detailedExplanation }}</div>
        </div>

        <!-- BP Reference Table -->
        <div class="mt-6">
          <h4 class="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">Tabel Klasifikasi Tekanan Darah (ACC/AHA 2017)</h4>
          <div class="overflow-x-auto -mx-2 px-2">
            <table class="w-full text-sm border-collapse">
              <thead>
                <tr class="bg-slate-50 dark:bg-slate-800/50">
                  <th class="text-left px-3 py-2.5 font-bold text-slate-600 dark:text-slate-300 rounded-tl-lg">Kategori</th>
                  <th class="text-center px-3 py-2.5 font-bold text-slate-600 dark:text-slate-300">Sistolik (mmHg)</th>
                  <th class="text-center px-3 py-2.5 font-bold text-slate-600 dark:text-slate-300 rounded-tr-lg">Diastolik (mmHg)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in bpReferenceTable" :key="row.category" 
                    :class="[isCurrentBPRow(row) ? 'bg-blue-50 dark:bg-blue-900/20 font-bold ring-2 ring-blue-500/30 ring-inset' : 'hover:bg-slate-50 dark:hover:bg-slate-800/30']"
                    class="border-t border-slate-100 dark:border-slate-800 transition-colors">
                  <td class="px-3 py-2.5 flex items-center gap-2">
                    <span :class="getTableDotColor(row.color)" class="w-2.5 h-2.5 rounded-full flex-shrink-0"></span>
                    <span class="text-slate-800 dark:text-slate-200">{{ row.category }}</span>
                    <span v-if="isCurrentBPRow(row)" class="text-[10px] bg-blue-100 dark:bg-blue-800 text-blue-700 dark:text-blue-300 px-1.5 py-0.5 rounded font-bold">PASIEN</span>
                  </td>
                  <td class="px-3 py-2.5 text-center text-slate-600 dark:text-slate-400 font-mono">{{ row.systolic }}</td>
                  <td class="px-3 py-2.5 text-center text-slate-600 dark:text-slate-400 font-mono">{{ row.diastolic }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- SECTION D: ANALISIS FAKTOR RISIKO                                -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div v-if="conclusion" class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20">
        <div class="flex items-center gap-3 mb-5">
          <div class="h-10 w-10 rounded-xl bg-orange-100 dark:bg-orange-500/20 text-orange-600 dark:text-orange-400 flex items-center justify-center text-lg">⚠️</div>
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Analisis Faktor Risiko</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Evaluasi 9 faktor risiko hipertensi berdasarkan data pasien</p>
          </div>
        </div>

        <!-- Risk Factor Summary Stats -->
        <div class="grid grid-cols-3 gap-3 mb-6">
          <div class="bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800/50 rounded-xl p-3 text-center">
            <p class="text-2xl font-black text-red-600 dark:text-red-400">{{ highRiskFactorCount }}</p>
            <p class="text-[10px] sm:text-xs font-bold text-red-500 dark:text-red-400 uppercase tracking-wider">Risiko Tinggi</p>
          </div>
          <div class="bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800/50 rounded-xl p-3 text-center">
            <p class="text-2xl font-black text-amber-600 dark:text-amber-400">{{ moderateRiskFactorCount }}</p>
            <p class="text-[10px] sm:text-xs font-bold text-amber-500 dark:text-amber-400 uppercase tracking-wider">Perlu Perhatian</p>
          </div>
          <div class="bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800/50 rounded-xl p-3 text-center">
            <p class="text-2xl font-black text-green-600 dark:text-green-400">{{ normalRiskFactorCount }}</p>
            <p class="text-[10px] sm:text-xs font-bold text-green-500 dark:text-green-400 uppercase tracking-wider">Normal</p>
          </div>
        </div>

        <!-- Risk Factor Cards -->
        <div class="space-y-3">
          <div v-for="factor in conclusion.riskFactors" :key="factor.id"
               :class="[factor.bgColor, factor.darkBgColor, factor.borderColor, factor.darkBorderColor]"
               class="rounded-xl border p-4 transition-all">
            <div class="flex items-start gap-3">
              <span class="text-xl flex-shrink-0 mt-0.5">{{ factor.icon }}</span>
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between flex-wrap gap-2 mb-1">
                  <h4 class="font-bold text-slate-900 dark:text-white text-sm">{{ factor.label }}</h4>
                  <span :class="[getStatusBadgeClass(factor.status)]" class="px-2 py-0.5 rounded-md text-[10px] sm:text-xs font-bold uppercase tracking-wider">{{ factor.statusLabel }}</span>
                </div>
                <p class="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">{{ factor.value }}</p>
                
                <!-- Expandable explanation -->
                <details class="group">
                  <summary class="text-xs text-slate-500 dark:text-slate-400 cursor-pointer hover:text-blue-600 dark:hover:text-blue-400 font-medium flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transition-transform group-open:rotate-90"><path d="m9 18 6-6-6-6"/></svg>
                    Penjelasan klinis
                  </summary>
                  <p class="text-xs text-slate-600 dark:text-slate-400 mt-2 leading-relaxed pl-4 border-l-2 border-slate-200 dark:border-slate-700">{{ factor.explanation }}</p>
                </details>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- SECTION E: FEATURE IMPORTANCE (XAI)                              -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div v-if="prediction?.feature_importance" class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20">
        <div class="flex items-center gap-3 mb-5">
          <div class="h-10 w-10 rounded-xl bg-indigo-100 dark:bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 flex items-center justify-center text-lg">🤖</div>
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Kontribusi Fitur Model AI (XAI)</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Feature importance — faktor yang paling mempengaruhi prediksi model</p>
          </div>
        </div>
        
        <div class="space-y-3">
          <div v-for="(feature, index) in sortedFeatures" :key="feature.feature" class="flex items-center gap-3">
            <span class="text-xs font-mono text-slate-400 dark:text-slate-500 w-5 text-right">{{ index + 1 }}</span>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-1">
                <span class="text-xs font-bold text-slate-700 dark:text-slate-300 truncate">{{ feature.label }}</span>
                <span class="text-xs font-mono text-slate-500 dark:text-slate-400 ml-2">{{ (feature.importance * 100).toFixed(1) }}%</span>
              </div>
              <div class="w-full bg-slate-100 dark:bg-slate-800 rounded-full h-2 overflow-hidden">
                <div class="h-full rounded-full transition-all duration-700 ease-out"
                     :class="index === 0 ? 'bg-gradient-to-r from-indigo-500 to-blue-500' : index <= 2 ? 'bg-blue-500' : 'bg-slate-400 dark:bg-slate-600'"
                     :style="{ width: `${Math.max(feature.importance / maxImportance * 100, 2)}%` }">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- SECTION F: RISIKO MASA DEPAN (10-Year CVD Risk)                  -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div v-if="conclusion" class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20">
        <div class="flex items-center gap-3 mb-5">
          <div class="h-10 w-10 rounded-xl bg-rose-100 dark:bg-rose-500/20 text-rose-600 dark:text-rose-400 flex items-center justify-center text-lg">📈</div>
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Estimasi Risiko Kardiovaskular 10 Tahun</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Proyeksi risiko penyakit jantung & stroke dalam dekade ke depan</p>
          </div>
        </div>

        <!-- Risk Gauge -->
        <div class="flex flex-col sm:flex-row items-center gap-6 mb-6">
          <!-- Visual Gauge -->
          <div class="relative h-32 w-32 sm:h-40 sm:w-40 flex-shrink-0">
            <svg class="h-full w-full" viewBox="0 0 120 120">
              <!-- Background arc -->
              <path d="M 15 90 A 50 50 0 1 1 105 90" fill="none" stroke-width="10" class="stroke-slate-200 dark:stroke-slate-800" stroke-linecap="round"/>
              <!-- Colored arc -->
              <path d="M 15 90 A 50 50 0 1 1 105 90" fill="none" stroke-width="10" stroke-linecap="round"
                    :class="getFutureRiskStrokeColor(conclusion.futureRiskLevel)"
                    :stroke-dasharray="`${(conclusion.futureRiskScore / 50) * 236} 236`"
                    class="transition-all duration-1000 ease-out"/>
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center pt-2">
              <span class="text-3xl sm:text-4xl font-black text-slate-900 dark:text-white">{{ conclusion.futureRiskScore }}%</span>
              <span :class="getFutureRiskTextColor(conclusion.futureRiskLevel)" class="text-xs font-bold uppercase tracking-wider">{{ conclusion.futureRiskLevel }}</span>
            </div>
          </div>

          <!-- Explanation -->
          <div class="flex-1">
            <p class="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">{{ conclusion.futureRiskExplanation }}</p>
            
            <div class="mt-4 p-3 bg-slate-50 dark:bg-slate-800/50 rounded-lg border border-slate-200 dark:border-slate-700">
              <p class="text-xs text-slate-500 dark:text-slate-400">
                <strong class="text-slate-700 dark:text-slate-300">Catatan:</strong> Estimasi ini dihitung berdasarkan faktor risiko yang tersedia dalam form skrining (usia, TD, BMI, merokok, diabetes, kolesterol, riwayat keluarga, aktivitas fisik). Untuk perhitungan risiko yang lebih akurat, gunakan Framingham Risk Score atau SCORE2 dengan data laboratorium lengkap (HDL, LDL, trigliserida).
              </p>
            </div>
          </div>
        </div>

        <!-- What happens if untreated -->
        <div v-if="conclusion.bpClassification.severity >= 2" class="bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-800/50 rounded-xl p-4 mt-4">
          <h4 class="text-sm font-bold text-red-800 dark:text-red-300 mb-2 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
            Risiko Jika Tidak Ditangani
          </h4>
          <ul class="text-xs text-red-700 dark:text-red-400 space-y-1.5 leading-relaxed">
            <li class="flex items-start gap-2"><span class="font-bold mt-0.5">•</span> Risiko stroke meningkat 2-4× lipat dibanding individu dengan tekanan darah normal</li>
            <li class="flex items-start gap-2"><span class="font-bold mt-0.5">•</span> Risiko serangan jantung (infark miokard) meningkat 2-3× lipat</li>
            <li class="flex items-start gap-2"><span class="font-bold mt-0.5">•</span> Risiko gagal ginjal kronis meningkat secara progresif</li>
            <li class="flex items-start gap-2"><span class="font-bold mt-0.5">•</span> Risiko gagal jantung kongestif meningkat 2-3× lipat</li>
            <li class="flex items-start gap-2"><span class="font-bold mt-0.5">•</span> Setiap kenaikan TDS 20 mmHg atau TDD 10 mmHg melipatduakan risiko kematian akibat penyakit kardiovaskular</li>
          </ul>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- SECTION G: REKOMENDASI PENANGANAN                                -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div v-if="conclusion && conclusion.recommendations.length > 0" class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20">
        <div class="flex items-center gap-3 mb-5">
          <div class="h-10 w-10 rounded-xl bg-emerald-100 dark:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-lg">💊</div>
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Rekomendasi Penanganan</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Intervensi non-farmakologis berdasarkan guideline medis internasional</p>
          </div>
        </div>

        <div class="space-y-3">
          <div v-for="rec in conclusion.recommendations" :key="rec.id"
               :class="[getRecPriorityBorder(rec.priority)]"
               class="rounded-xl border p-4 bg-white dark:bg-slate-900 transition-all">
            <div class="flex items-start gap-3">
              <span class="text-xl flex-shrink-0 mt-0.5">{{ rec.icon }}</span>
              <div class="flex-1 min-w-0">
                <div class="flex items-center flex-wrap gap-2 mb-1">
                  <span class="text-[10px] font-bold uppercase tracking-widest text-slate-400 dark:text-slate-500">{{ rec.category }}</span>
                  <span :class="[getRecPriorityBadge(rec.priority)]" class="px-1.5 py-0.5 rounded text-[9px] sm:text-[10px] font-bold uppercase tracking-wider">
                    {{ rec.priority === 'critical' ? 'Prioritas Utama' : rec.priority === 'important' ? 'Penting' : 'Disarankan' }}
                  </span>
                </div>
                <h4 class="font-bold text-slate-900 dark:text-white text-sm mb-1">{{ rec.title }}</h4>
                <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{{ rec.description }}</p>
                <div v-if="rec.target" class="mt-2 flex items-center gap-1.5 text-xs font-semibold text-blue-600 dark:text-blue-400">
                  <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
                  {{ rec.target }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- SECTION H: RENCANA TINDAK LANJUT                                 -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div v-if="conclusion" class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-white dark:bg-slate-900 p-6 sm:p-8 shadow-lg shadow-slate-200/20 dark:shadow-slate-900/20">
        <div class="flex items-center gap-3 mb-5">
          <div class="h-10 w-10 rounded-xl bg-teal-100 dark:bg-teal-500/20 text-teal-600 dark:text-teal-400 flex items-center justify-center text-lg">📅</div>
          <div>
            <h3 class="text-lg font-bold text-slate-900 dark:text-white">Rencana Tindak Lanjut</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Jadwal kontrol, pemeriksaan tambahan, dan target terapi</p>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
          <div class="bg-slate-50 dark:bg-slate-800/50 rounded-xl p-4 border border-slate-200 dark:border-slate-700">
            <p class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">Kontrol Berikutnya</p>
            <p class="text-sm font-bold text-slate-900 dark:text-white">{{ conclusion.followUpPlan.nextVisit }}</p>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800/50 rounded-xl p-4 border border-slate-200 dark:border-slate-700">
            <p class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-1">Frekuensi Monitoring</p>
            <p class="text-sm font-bold text-slate-900 dark:text-white">{{ conclusion.followUpPlan.frequency }}</p>
          </div>
          <div class="sm:col-span-2 bg-blue-50 dark:bg-blue-950/30 rounded-xl p-4 border border-blue-200 dark:border-blue-800/50">
            <p class="text-xs font-bold uppercase tracking-wider text-blue-500 dark:text-blue-400 mb-1">Target Tekanan Darah</p>
            <p class="text-sm font-bold text-blue-900 dark:text-blue-200">{{ conclusion.followUpPlan.targetBP }}</p>
          </div>
        </div>

        <!-- Additional Tests -->
        <div class="mb-6">
          <h4 class="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">Pemeriksaan Tambahan yang Disarankan</h4>
          <div class="space-y-2">
            <div v-for="(test, i) in conclusion.followUpPlan.additionalTests" :key="i" class="flex items-start gap-2.5 text-sm">
              <div class="h-5 w-5 rounded-md bg-teal-100 dark:bg-teal-900/30 text-teal-600 dark:text-teal-400 flex items-center justify-center flex-shrink-0 mt-0.5 text-xs font-bold">{{ i + 1 }}</div>
              <span class="text-slate-700 dark:text-slate-300 text-xs leading-relaxed">{{ test }}</span>
            </div>
          </div>
        </div>

        <!-- Lifestyle Monitoring -->
        <div>
          <h4 class="text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">Monitoring Gaya Hidup</h4>
          <div class="space-y-2">
            <div v-for="(item, i) in conclusion.followUpPlan.lifestyle" :key="i" class="flex items-center gap-2.5 text-sm">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="text-teal-500 flex-shrink-0"><path d="M20 6 9 17l-5-5"/></svg>
              <span class="text-slate-700 dark:text-slate-300 text-xs">{{ item }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <!-- FOOTER DISCLAIMER                                                -->
      <!-- ═══════════════════════════════════════════════════════════════════ -->
      <div class="rounded-2xl border border-slate-200/60 dark:border-slate-800/60 bg-slate-50 dark:bg-slate-900/50 p-6 text-center space-y-3">
        <div class="flex items-center justify-center gap-2 mb-2">
          <div class="h-6 w-6 bg-blue-600 rounded-lg flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.48 12H2"/></svg>
          </div>
          <span class="font-bold text-sm text-slate-700 dark:text-slate-300">HT-Detect — Sistem Deteksi Dini Hipertensi</span>
        </div>
        <p class="text-[11px] text-slate-400 dark:text-slate-500 leading-relaxed max-w-lg mx-auto">
          Laporan ini dihasilkan secara otomatis oleh model AI (XGBoost dioptimasi SGO) dan interpretasi klinis berdasarkan Pedoman PERKI (Indonesia), WHO, dan ESC/ESH. 
          Hasil ini <strong class="text-slate-500 dark:text-slate-400">BUKAN merupakan diagnosis klinis</strong> dan harus dikonsultasikan dengan dokter untuk evaluasi dan penatalaksanaan lebih lanjut.
        </p>
        <p class="text-[10px] text-slate-400 dark:text-slate-500">
          Dikembangkan oleh Samuel Alfred Richardo Napitupulu — D4 TRPL, Politeknik Negeri Medan
        </p>
      </div>

    </div>
    <!-- ═══ PDF CONTENT END ═══ -->

    <!-- Bottom Action Bar -->
    <div class="flex justify-end pt-4">
      <button @click="downloadPDF" :disabled="downloading" class="bg-gradient-to-r from-indigo-600 to-blue-600 hover:from-indigo-700 hover:to-blue-700 text-white px-6 py-3 rounded-xl text-sm font-bold transition-all flex items-center gap-2 shadow-lg shadow-indigo-500/20 active:scale-95 disabled:opacity-60">
        <svg v-if="downloading" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
        <span>{{ downloading ? 'Memproses Laporan...' : 'Unduh Laporan PDF' }}</span>
      </button>
    </div>

  </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { screeningService } from '../../services/screeningService'
import {
  generateClinicalConclusion,
  BP_REFERENCE_TABLE,
  type ScreeningData,
  type PredictionData,
  type ClinicalConclusion,
} from '../../lib/clinicalUtils'

// Dynamic import html2pdf so it doesn't break SSR (though this is SPA, it's safer)
let html2pdf: any;
if (typeof window !== 'undefined') {
  import('html2pdf.js').then(module => {
    html2pdf = module.default;
  });
}

const route = useRoute()
const router = useRouter()
const screening = ref<any>(null)
const downloading = ref(false)
const conclusion = ref<ClinicalConclusion | null>(null)
const loadError = ref('')

// Label Indonesia untuk kode fitur dari ML engine / fallback lokal
const FEATURE_LABELS: Record<string, string> = {
  systolic_bp: 'Tekanan Darah Sistolik',
  diastolic_bp: 'Tekanan Darah Diastolik',
  bmi: 'Indeks Massa Tubuh (IMT)',
  age: 'Usia',
  salt_consumption: 'Konsumsi Garam',
  family_history: 'Riwayat Keluarga',
  smoking_status: 'Status Merokok',
  red_meat_consumption: 'Konsumsi Daging Merah',
  physical_activity: 'Aktivitas Fisik',
  gender: 'Jenis Kelamin',
}

// Reference table data
const bpReferenceTable = BP_REFERENCE_TABLE

// Fetch screening data and generate clinical interpretation
const fetchScreening = async () => {
  loadError.value = ''
  try {
    // getScreening otomatis membaca hasil lokal untuk id "local-..." dan
    // memanggil API backend untuk id numerik.
    const response: any = await screeningService.getScreening(String(route.params.id))
    if (!response.data) throw new Error('Data skrining kosong.')
    screening.value = response.data
  } catch (e: any) {
    console.error('Gagal memuat hasil skrining', e)
    loadError.value =
      e?.response?.status === 404
        ? 'Hasil skrining tidak ditemukan.'
        : 'Gagal memuat hasil skrining. Pastikan backend berjalan, lalu coba lagi.'
    return
  }

  // Generate clinical conclusion from screening data
  if (screening.value) {
    const screeningData: ScreeningData = {
      age: Number(screening.value.age || 0),
      gender: screening.value.gender || 'male',
      bmi: Number(screening.value.bmi || 0),
      smoking_status: Boolean(screening.value.smoking_status),
      physical_activity: screening.value.physical_activity || 'low',
      family_history: Boolean(screening.value.family_history),
      red_meat_consumption: screening.value.red_meat_consumption || 'low',
      salt_consumption: screening.value.salt_consumption || 'low',
      systolic_bp: Number(screening.value.systolic_bp || 120),
      diastolic_bp: Number(screening.value.diastolic_bp || 80),
    }

    const predictionData: PredictionData = {
      risk_level: screening.value.prediction?.risk_level || 'low',
      confidence_score: Number(screening.value.prediction?.confidence_score || 0),
      probability: screening.value.prediction?.probability_distribution || {},
      feature_importance: screening.value.prediction?.feature_importance || [],
    }

    conclusion.value = generateClinicalConclusion(screeningData, predictionData)
  }
}

// Computed properties
const prediction = computed(() => screening.value?.prediction)

const sortedFeatures = computed(() => {
  if (!prediction.value?.feature_importance) return []
  return [...prediction.value.feature_importance]
    .map((f: any) => ({ ...f, label: f.label || FEATURE_LABELS[f.feature] || f.feature }))
    .sort((a: any, b: any) => Math.abs(b.importance) - Math.abs(a.importance))
})

const maxImportance = computed(() => {
  if (sortedFeatures.value.length === 0) return 1
  return Math.abs(sortedFeatures.value[0].importance)
})

const highRiskFactorCount = computed(() =>
  conclusion.value?.riskFactors.filter((f) => f.status === 'high').length || 0
)
const moderateRiskFactorCount = computed(() =>
  conclusion.value?.riskFactors.filter((f) => f.status === 'moderate').length || 0
)
const normalRiskFactorCount = computed(() =>
  conclusion.value?.riskFactors.filter((f) => f.status === 'normal').length || 0
)

// Helper functions
const formatDate = (dateString?: string) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return '-'
  return date.toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getRiskBannerClass = (category?: string) => {
  if (['stage2', 'crisis'].includes(category || '')) return 'bg-gradient-to-br from-red-600 to-rose-700 text-white'
  if (['elevated', 'stage1'].includes(category || '')) return 'bg-gradient-to-br from-amber-500 to-orange-600 text-white'
  return 'bg-gradient-to-br from-emerald-500 to-green-600 text-white'
}

const getRiskSummaryClass = (category?: string) => {
  if (['stage2', 'crisis'].includes(category || '')) return 'bg-red-50 dark:bg-red-950/30 border-red-200 dark:border-red-800/50 text-red-800 dark:text-red-300'
  if (['elevated', 'stage1'].includes(category || '')) return 'bg-amber-50 dark:bg-amber-950/30 border-amber-200 dark:border-amber-800/50 text-amber-800 dark:text-amber-300'
  return 'bg-green-50 dark:bg-green-950/30 border-green-200 dark:border-green-800/50 text-green-800 dark:text-green-300'
}

const getStatusBadgeClass = (status: string) => {
  if (status === 'high') return 'bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-400'
  if (status === 'moderate') return 'bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-400'
  return 'bg-green-100 dark:bg-green-900/40 text-green-700 dark:text-green-400'
}

const getTableDotColor = (color: string) => {
  const map: Record<string, string> = {
    green: 'bg-green-500',
    amber: 'bg-amber-500',
    orange: 'bg-orange-500',
    red: 'bg-red-500',
    rose: 'bg-rose-500',
  }
  return map[color] || 'bg-slate-400'
}

const isCurrentBPRow = (row: { category: string }) => {
  if (!conclusion.value) return false
  const label = conclusion.value.bpClassification.label
  // Match based on BP category label
  return row.category === label || row.category.includes(label) || label.includes(row.category)
}

const getFutureRiskStrokeColor = (level: string) => {
  if (level === 'Sangat Tinggi' || level === 'Tinggi') return 'stroke-red-500'
  if (level === 'Sedang') return 'stroke-amber-500'
  return 'stroke-green-500'
}

const getFutureRiskTextColor = (level: string) => {
  if (level === 'Sangat Tinggi' || level === 'Tinggi') return 'text-red-600 dark:text-red-400'
  if (level === 'Sedang') return 'text-amber-600 dark:text-amber-400'
  return 'text-green-600 dark:text-green-400'
}

const getRecPriorityBorder = (priority: string) => {
  if (priority === 'critical') return 'border-red-200 dark:border-red-800/50 bg-red-50/30 dark:bg-red-950/10'
  if (priority === 'important') return 'border-amber-200 dark:border-amber-800/50 bg-amber-50/30 dark:bg-amber-950/10'
  return 'border-slate-200 dark:border-slate-700 bg-slate-50/30 dark:bg-slate-800/30'
}

const getRecPriorityBadge = (priority: string) => {
  if (priority === 'critical') return 'bg-red-100 dark:bg-red-900/40 text-red-700 dark:text-red-400'
  if (priority === 'important') return 'bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-400'
  return 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'
}

const downloadPDF = async () => {
  if (!html2pdf) {
    alert('Modul PDF sedang dimuat, silakan coba lagi dalam beberapa detik.');
    return;
  }
  
  downloading.value = true
  try {
    const element = document.getElementById('pdf-content')
    const opt = {
      margin:       [8, 8, 8, 8],
      filename:     `Laporan-Skrining-Hipertensi-${screening.value.patient?.nik || screening.value.nik || 'unknown'}.pdf`,
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2, useCORS: true, logging: false },
      jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' },
      pagebreak:    { mode: ['avoid-all', 'css', 'legacy'] }
    }
    
    await html2pdf().set(opt).from(element).save()
  } catch (error) {
    console.error("Failed to generate PDF", error)
  } finally {
    downloading.value = false
  }
}

onMounted(() => {
  fetchScreening()
})
</script>
