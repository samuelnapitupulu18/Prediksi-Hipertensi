
<template>
  <div class="mx-auto max-w-3xl">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Skrining Klinis</h2>
        <p class="text-sm text-slate-500 dark:text-slate-400 mt-1">Evaluasi 10 atribut risiko hipertensi dengan model prediksi XGBoost.</p>
      </div>
      <div class="flex items-center gap-2 bg-blue-50 dark:bg-blue-900/30 px-3 py-1.5 rounded-full border border-blue-100 dark:border-blue-800">
        <span class="text-sm font-bold text-blue-700 dark:text-blue-400">Langkah {{ step }} dari 3</span>
      </div>
    </div>

    <!-- Sticky Progress Bar with Glow -->
    <div class="sticky top-0 z-20 bg-slate-50 dark:bg-slate-950 py-4 -mx-4 px-4 sm:mx-0 sm:px-0 transition-colors mb-8">
      <div class="w-full bg-slate-100 dark:bg-slate-800 h-3 rounded-full overflow-hidden shadow-inner relative">
        <div class="absolute top-0 left-0 h-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all duration-500 ease-out shadow-[0_0_10px_rgba(79,70,229,0.5)]" :style="{ width: `${(step / 3) * 100}%` }"></div>
      </div>
    </div>

    <!-- Form Container -->
    <div class="rounded-3xl border border-slate-200/50 dark:border-slate-800/50 bg-white/70 dark:bg-slate-900/70 backdrop-blur-xl p-6 sm:p-10 shadow-xl shadow-slate-200/40 dark:shadow-slate-900/40 transition-colors">
      <form @submit.prevent="onSubmit" :class="{ 'animate-shake': formErrors }">
        
        <!-- STEP 1: Demografi & Antropometri -->
        <div v-show="step === 1" class="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
          <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div class="h-10 w-10 rounded-xl bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">1</div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">Demografi & Fisik</h3>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Identitas -->
            <div class="md:col-span-2 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">NIK (Nomor Induk Kependudukan)</label>
              <input type="text" inputmode="numeric" v-model="formData.nik" class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-blue-500 outline-none font-mono tracking-wide" placeholder="16 digit NIK" maxlength="16" />
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400">Tanggal lahir & jenis kelamin terisi otomatis dari NIK (format Dukcapil: digit ke-7 s/d 12 adalah tanggal lahir).</p>
              <p v-if="errors.nik" class="text-xs font-medium text-red-500">{{ errors.nik }}</p>
            </div>

            <div class="md:col-span-2 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Nama Lengkap</label>
              <input type="text" v-model="formData.name" class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Nama sesuai KTP" />
              <p v-if="errors.name" class="text-xs font-medium text-red-500">{{ errors.name }}</p>
            </div>
            
            <div class="md:col-span-1 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Tanggal Lahir</label>
              <div class="w-full px-4 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/60 font-semibold" :class="formattedDob ? 'text-slate-800 dark:text-slate-200' : 'text-slate-400 dark:text-slate-500'">
                {{ formattedDob || 'Terbaca otomatis dari NIK' }}
              </div>
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400">Tidak perlu diisi manual — dibaca dari NIK.</p>
              <p v-if="errors.date_of_birth" class="text-xs font-medium text-red-500">{{ errors.date_of_birth }}</p>
            </div>

            <!-- Usia -->
            <div class="md:col-span-1 space-y-3">
              <label class="flex items-center justify-between text-sm font-bold text-slate-700 dark:text-slate-300">
                <span>Usia (Tahun)</span>
                <span class="text-xl font-black text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 px-3 py-1 rounded-lg border border-blue-100 dark:border-blue-800">{{ formData.age }}</span>
              </label>
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mt-2">Dihitung otomatis dari tanggal lahir.</p>
              <p v-if="errors.age" class="text-xs font-medium text-red-500 animate-in slide-in-from-top-1">{{ errors.age }}</p>
            </div>

            <!-- Jenis Kelamin -->
            <div class="md:col-span-1 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Jenis Kelamin</label>
              <div class="grid grid-cols-2 gap-3">
                <label class="relative cursor-pointer">
                  <input type="radio" v-model="formData.gender" value="male" class="peer sr-only" name="gender" />
                  <div class="rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-3 text-center transition-all peer-checked:border-blue-600 peer-checked:bg-blue-50 dark:peer-checked:bg-blue-900/20 peer-checked:text-blue-700 dark:peer-checked:text-blue-400 hover:bg-slate-50 dark:hover:bg-slate-700/50">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-2"><circle cx="10" cy="10" r="6"/><path d="m14 14 7 7"/><path d="m14 21 7-7"/></svg>
                    <span class="font-semibold text-sm">Laki-laki</span>
                  </div>
                </label>
                <label class="relative cursor-pointer">
                  <input type="radio" v-model="formData.gender" value="female" class="peer sr-only" name="gender" />
                  <div class="rounded-xl border-2 border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-3 text-center transition-all peer-checked:border-pink-500 peer-checked:bg-pink-50 dark:peer-checked:bg-pink-900/20 peer-checked:text-pink-600 dark:peer-checked:text-pink-400 hover:bg-slate-50 dark:hover:bg-slate-700/50">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mx-auto mb-2"><circle cx="12" cy="10" r="6"/><path d="M12 16v6"/><path d="M9 19h6"/></svg>
                    <span class="font-semibold text-sm">Perempuan</span>
                  </div>
                </label>
              </div>
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400">Terisi otomatis dari NIK, dapat diubah bila diperlukan.</p>
              <p v-if="errors.gender" class="text-xs font-medium text-red-500 animate-in slide-in-from-top-1">{{ errors.gender }}</p>
            </div>

            <!-- BMI -->
            <div class="md:col-span-2 space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Pengukuran Fisik (IMT Otomatis)</label>
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-1">
                  <span class="text-xs text-slate-500 font-medium">Berat Badan</span>
                  <div class="relative">
                    <input type="number" v-model.number="formData.weight" class="block w-full rounded-xl border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-white py-3 px-4 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all" :class="{'border-red-500 bg-red-50 dark:bg-red-900/10': errors.weight}" placeholder="65" />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none text-sm font-medium text-slate-400">kg</div>
                  </div>
                  <p v-if="errors.weight" class="text-xs font-medium text-red-500 mt-1">{{ errors.weight }}</p>
                </div>
                <div class="space-y-1">
                  <span class="text-xs text-slate-500 font-medium">Tinggi Badan</span>
                  <div class="relative">
                    <input type="number" v-model.number="formData.height" class="block w-full rounded-xl border border-slate-200 dark:border-slate-700 dark:bg-slate-800 dark:text-white py-3 px-4 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 outline-none transition-all" :class="{'border-red-500 bg-red-50 dark:bg-red-900/10': errors.height}" placeholder="165" />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none text-sm font-medium text-slate-400">cm</div>
                  </div>
                  <p v-if="errors.height" class="text-xs font-medium text-red-500 mt-1">{{ errors.height }}</p>
                </div>
              </div>
              <div class="flex items-center justify-between bg-blue-50 dark:bg-blue-900/20 p-3 rounded-xl mt-2 border border-blue-100 dark:border-blue-800/50">
                <span class="text-sm font-semibold text-blue-800 dark:text-blue-300">Hasil Indeks Massa Tubuh (IMT):</span>
                <div class="text-right">
                  <span class="text-lg font-black text-blue-700 dark:text-blue-400">{{ formData.bmi }} <span class="text-sm font-semibold text-blue-500 dark:text-blue-300">kg/m²</span></span>
                  <p class="text-xs font-bold text-blue-600 dark:text-blue-300">{{ bmiCategoryLabel }}</p>
                </div>
              </div>
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400">Kategori IMT mengikuti standar WHO Asia-Pasifik.</p>
            </div>
          </div>
        </div>

        <!-- STEP 2: Gaya Hidup & Riwayat -->
        <div v-show="step === 2" class="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
          <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div class="h-10 w-10 rounded-xl bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">2</div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">Gaya Hidup & Pola Makan</h3>
          </div>
          
          <div class="grid grid-cols-1 gap-8">
            <div class="space-y-3">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Aktivitas Fisik / Olahraga <span class="font-medium text-slate-400">(dihitung per minggu)</span></label>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <label v-for="opt in activityOptions" :key="opt.v" class="flex items-start p-3 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" :class="{'border-blue-500 bg-blue-50/50 dark:bg-blue-900/20': formData.physical_activity === opt.v}">
                  <input type="radio" v-model="formData.physical_activity" :value="opt.v" class="w-4 h-4 mt-1 text-blue-600 accent-blue-600" />
                  <span class="ml-3">
                    <span class="block font-medium text-slate-700 dark:text-slate-300">{{ opt.l }}</span>
                    <span class="block text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ opt.d }}</span>
                  </span>
                </label>
              </div>
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400">Satu sesi olahraga minimal ±30 menit (jalan cepat, bersepeda, senam). Anjuran PERKI: aktivitas fisik ≥ 5 kali/minggu (total ±150 menit/minggu).</p>
            </div>

            <!-- iOS style switches with Card Look -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              
              <div class="flex items-center justify-between p-5 border border-slate-200 dark:border-slate-700 rounded-2xl bg-gradient-to-br from-white to-slate-50 dark:from-slate-800 dark:to-slate-800/80 shadow-sm">
                <div>
                  <p class="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-blue-500"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                    Riwayat Diabetes
                  </p>
                  <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mt-1">Ada riwayat diabetes di keluarga?</p>
                </div>
                <label class="relative inline-flex cursor-pointer items-center">
                  <input type="checkbox" v-model="formData.family_history" class="peer sr-only" />
                  <div class="w-14 h-7 rounded-full bg-slate-200 dark:bg-slate-700 peer-checked:bg-blue-600 after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border after:border-slate-300 after:rounded-full after:h-6 after:w-6 after:transition-all after:shadow-sm peer-checked:after:translate-x-7 peer-checked:after:border-white"></div>
                </label>
              </div>

              <div class="flex items-center justify-between p-5 border border-slate-200 dark:border-slate-700 rounded-2xl bg-gradient-to-br from-white to-slate-50 dark:from-slate-800 dark:to-slate-800/80 shadow-sm">
                <div>
                  <p class="font-bold text-slate-900 dark:text-white flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-rose-500"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg>
                    Status Perokok
                  </p>
                  <p class="text-xs font-medium text-slate-500 dark:text-slate-400 mt-1">Apakah pasien perokok aktif?</p>
                </div>
                <label class="relative inline-flex cursor-pointer items-center">
                  <input type="checkbox" v-model="formData.smoking_status" class="peer sr-only" />
                  <div class="w-14 h-7 rounded-full bg-slate-200 dark:bg-slate-700 peer-checked:bg-rose-500 after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border after:border-slate-300 after:rounded-full after:h-6 after:w-6 after:transition-all after:shadow-sm peer-checked:after:translate-x-7 peer-checked:after:border-white"></div>
                </label>
              </div>

            </div>

            <div class="space-y-3 mt-4">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Konsumsi Daging Merah <span class="font-medium text-slate-400">(dihitung per minggu)</span></label>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <label v-for="opt in redMeatOptions" :key="opt.v" class="flex items-start p-3 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" :class="{'border-blue-500 bg-blue-50/50 dark:bg-blue-900/20': formData.red_meat_consumption === opt.v}">
                  <input type="radio" v-model="formData.red_meat_consumption" :value="opt.v" class="w-4 h-4 mt-1 text-blue-600 accent-blue-600" />
                  <span class="ml-3">
                    <span class="block font-medium text-slate-700 dark:text-slate-300">{{ opt.l }}</span>
                    <span class="block text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ opt.d }}</span>
                  </span>
                </label>
              </div>
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400">1 porsi ≈ 50–70 gram daging matang (sapi, kambing, atau olahannya). PERKI menganjurkan membatasi daging merah & lemak jenuh.</p>
            </div>

            <div class="space-y-3 mt-4">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Konsumsi Garam <span class="font-medium text-slate-400">(dihitung per minggu)</span></label>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <label v-for="opt in saltOptions" :key="opt.v" class="flex items-start p-3 rounded-xl border border-slate-200 dark:border-slate-700 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors" :class="{'border-blue-500 bg-blue-50/50 dark:bg-blue-900/20': formData.salt_consumption === opt.v}">
                  <input type="radio" v-model="formData.salt_consumption" :value="opt.v" class="w-4 h-4 mt-1 text-blue-600 accent-blue-600" />
                  <span class="ml-3">
                    <span class="block font-medium text-slate-700 dark:text-slate-300">{{ opt.l }}</span>
                    <span class="block text-xs text-slate-500 dark:text-slate-400 mt-0.5">{{ opt.d }}</span>
                  </span>
                </label>
              </div>
              <p class="text-xs font-medium text-slate-500 dark:text-slate-400">Batas anjuran PERKI/WHO: &lt; 5 gram garam per hari (≈ 1 sendok teh) atau &lt; 35 gram per minggu. Sudah termasuk garam dalam masakan, kecap, dan makanan olahan.</p>
            </div>

          </div>
        </div>

        <!-- STEP 3: Pengukuran Klinis -->
        <div v-show="step === 3" class="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
          <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div class="h-10 w-10 rounded-xl bg-blue-100 dark:bg-blue-500/20 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold text-lg">3</div>
            <h3 class="text-xl font-bold text-slate-900 dark:text-white">Pengukuran Klinis (Tensi)</h3>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="md:col-span-1 space-y-3 relative">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Sistolik (mmHg)</label>
              <div class="relative">
                <input type="number" v-model.number="formData.systolic_bp" class="block w-full rounded-xl border-slate-300 dark:border-slate-700 dark:bg-slate-800 dark:text-white py-3.5 px-4 border shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 sm:text-lg font-mono transition-all" :class="{'border-red-500 ring-2 ring-red-500/20 bg-red-50 dark:bg-red-900/10': errors.systolic_bp}" placeholder="120" />
                <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
                  <span class="text-slate-400 font-medium">SYS</span>
                </div>
              </div>
              <p v-if="errors.systolic_bp" class="text-xs font-medium text-red-500 mt-1 animate-in slide-in-from-top-1">{{ errors.systolic_bp }}</p>
            </div>
            
            <div class="md:col-span-1 space-y-3 relative">
              <label class="block text-sm font-bold text-slate-700 dark:text-slate-300">Diastolik (mmHg)</label>
              <div class="relative">
                <input type="number" v-model.number="formData.diastolic_bp" class="block w-full rounded-xl border-slate-300 dark:border-slate-700 dark:bg-slate-800 dark:text-white py-3.5 px-4 border shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 sm:text-lg font-mono transition-all" :class="{'border-red-500 ring-2 ring-red-500/20 bg-red-50 dark:bg-red-900/10': errors.diastolic_bp}" placeholder="80" />
                <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
                  <span class="text-slate-400 font-medium">DIA</span>
                </div>
              </div>
              <p v-if="errors.diastolic_bp" class="text-xs font-medium text-red-500 mt-1 animate-in slide-in-from-top-1">{{ errors.diastolic_bp }}</p>
            </div>
          </div>
        </div>

        <!-- Submit Error Banner -->
        <div v-if="submitError" class="mt-8 p-4 rounded-xl border border-red-200 dark:border-red-800/50 bg-red-50 dark:bg-red-950/30 flex items-start gap-3">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-red-500 flex-shrink-0 mt-0.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <p class="text-sm font-medium text-red-700 dark:text-red-300">{{ submitError }}</p>
        </div>

        <!-- Form Actions -->
        <div class="mt-10 pt-6 flex items-center justify-between border-t border-slate-100 dark:border-slate-800">
          <button type="button" @click="prevStep" :disabled="step === 1" class="px-6 py-3 text-sm font-bold text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl shadow-sm hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-0 disabled:pointer-events-none transition-all active:scale-95">
            &larr; Kembali
          </button>
          
          <button v-if="step < 3" type="button" @click="nextStep" class="px-8 py-3 text-sm font-bold text-white bg-blue-600 rounded-xl shadow-lg shadow-blue-500/30 hover:bg-blue-700 hover:shadow-blue-500/50 transition-all active:scale-95 flex items-center gap-2 ml-auto">
            Selanjutnya &rarr;
          </button>
          
          <button v-if="step === 3" type="submit" :disabled="isSubmitting" class="px-8 py-3 text-sm font-bold text-white bg-gradient-to-r from-indigo-600 to-blue-600 rounded-xl shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 dark:focus:ring-offset-slate-900 disabled:opacity-70 transition-all active:scale-95 flex items-center gap-2 ml-auto">
            <svg v-if="isSubmitting" class="h-5 w-5 animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            {{ isSubmitting ? 'Menganalisis...' : 'Proses' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { z } from 'zod'
import { screeningService } from '../../services/screeningService'
import { classifyBMI } from '../../lib/clinicalUtils'

const router = useRouter()
const route = useRoute()
const step = ref(1)
const isSubmitting = ref(false)
const formErrors = ref(false)

// Opsi gaya hidup dengan keterangan frekuensi per minggu (kesepakatan mengacu PERKI)
const activityOptions = [
  { v: 'low', l: 'Rendah', d: '≤ 1 kali / minggu' },
  { v: 'moderate', l: 'Sedang', d: '2–4 kali / minggu' },
  { v: 'high', l: 'Tinggi', d: '≥ 5 kali / minggu' },
]

const redMeatOptions = [
  { v: 'low', l: 'Jarang', d: '≤ 1 porsi / minggu' },
  { v: 'moderate', l: 'Sedang', d: '2–4 porsi / minggu' },
  { v: 'high', l: 'Sering', d: '≥ 5 porsi / minggu' },
]

const saltOptions = [
  { v: 'low', l: 'Rendah', d: '< 35 gram / minggu' },
  { v: 'moderate', l: 'Sedang', d: '35–42 gram / minggu' },
  { v: 'high', l: 'Tinggi', d: '> 42 gram / minggu' },
]

// Data state
const formData = reactive({
  nik: '',
  name: '',
  date_of_birth: '',
  age: 0,
  gender: '',
  bmi: 0,
  family_history: false,
  physical_activity: '',
  smoking_status: false,
  red_meat_consumption: '',
  salt_consumption: '',
  systolic_bp: null as number | null,
  diastolic_bp: null as number | null,
  weight: null as number | null,
  height: null as number | null
})

// ─── Pembacaan NIK sesuai format Dukcapil (16 digit) ───
// Digit 1-6: kode wilayah, digit 7-12: tanggal lahir DDMMYY
// (untuk perempuan, DD ditambah 40), digit 13-16: nomor urut.
const parseNIK = (nik: string): { dob: string; gender: 'male' | 'female' } | null => {
  if (!/^\d{16}$/.test(nik)) return null
  let day = Number(nik.slice(6, 8))
  const month = Number(nik.slice(8, 10))
  const yy = Number(nik.slice(10, 12))
  const isFemale = day > 40
  if (isFemale) day -= 40
  const currentYY = new Date().getFullYear() % 100
  const year = yy <= currentYY ? 2000 + yy : 1900 + yy
  // Validasi tanggal benar-benar ada di kalender
  const date = new Date(year, month - 1, day)
  if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) return null
  const pad = (n: number) => String(n).padStart(2, '0')
  return { dob: `${year}-${pad(month)}-${pad(day)}`, gender: isFemale ? 'female' : 'male' }
}

// Tanggal lahir & jenis kelamin otomatis terbaca dari NIK
watch(() => formData.nik, (nik) => {
  const digitsOnly = nik.replace(/\D/g, '')
  if (digitsOnly !== nik) {
    formData.nik = digitsOnly
    return
  }
  const parsed = parseNIK(nik)
  if (parsed) {
    formData.date_of_birth = parsed.dob
    formData.gender = parsed.gender
  } else {
    formData.date_of_birth = ''
  }
})

const formattedDob = computed(() => {
  if (!formData.date_of_birth) return ''
  const d = new Date(formData.date_of_birth)
  if (isNaN(d.getTime())) return ''
  return d.toLocaleDateString('id-ID', { day: 'numeric', month: 'long', year: 'numeric' })
})

// Kategori IMT (WHO Asia-Pasifik) untuk ditampilkan bersama hasil IMT
const bmiCategoryLabel = computed(() => {
  if (!formData.bmi || formData.bmi <= 0) return '-'
  return classifyBMI(formData.bmi).label
})

// Calculate age automatically when date of birth changes
watch(() => formData.date_of_birth, (newDate) => {
  if (newDate) {
    const dob = new Date(newDate)
    const today = new Date()
    let age = today.getFullYear() - dob.getFullYear()
    const m = today.getMonth() - dob.getMonth()
    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
      age--
    }
    formData.age = age > 0 ? age : 0
  } else {
    formData.age = 0
  }
})

// Calculate BMI automatically
watch([() => formData.weight, () => formData.height], ([newWeight, newHeight]) => {
  if (newWeight && newHeight && newWeight > 0 && newHeight > 0) {
    const heightInMeters = newHeight / 100;
    formData.bmi = Number((newWeight / (heightInMeters * heightInMeters)).toFixed(1));
  } else {
    formData.bmi = 0;
  }
})

// Validation State
const errors = reactive<Record<string, string>>({})

// Zod Schemas per step for partial validation
const step1Schema = z.object({
  nik: z.string().regex(/^\d{16}$/, 'NIK harus 16 digit angka'),
  name: z.string().min(3, 'Nama minimal 3 karakter'),
  date_of_birth: z.string().min(1, 'Tanggal lahir tidak terbaca dari NIK — periksa kembali digit ke-7 s/d 12'),
  age: z.number().min(18, 'Minimal usia 18 tahun').max(100),
  gender: z.string().min(1, 'Jenis kelamin wajib dipilih'),
  weight: z.number({ required_error: 'Berat badan wajib diisi', invalid_type_error: 'Berat badan wajib diisi' }).min(20, 'Berat badan minimal 20kg').max(300, 'Berat badan tidak valid'),
  height: z.number({ required_error: 'Tinggi badan wajib diisi', invalid_type_error: 'Tinggi badan wajib diisi' }).min(50, 'Tinggi badan minimal 50cm').max(300, 'Tinggi badan tidak valid'),
  bmi: z.number().min(10).max(60)
})

const step2Schema = z.object({
  physical_activity: z.string().min(1, 'Aktivitas fisik wajib dipilih'),
  red_meat_consumption: z.string().min(1, 'Konsumsi daging merah wajib dipilih'),
  salt_consumption: z.string().min(1, 'Konsumsi garam wajib dipilih'),
})

const step3Schema = z.object({
  systolic_bp: z.number({ required_error: 'Tekanan sistolik wajib diisi', invalid_type_error: 'Tekanan sistolik wajib diisi' }).min(70, 'Sistolik terlalu rendah').max(250, 'Sistolik terlalu tinggi'),
  diastolic_bp: z.number({ required_error: 'Tekanan diastolik wajib diisi', invalid_type_error: 'Tekanan diastolik wajib diisi' }).min(40, 'Diastolik terlalu rendah').max(150, 'Diastolik terlalu tinggi'),
})

const triggerShake = () => {
  formErrors.value = true
  setTimeout(() => { formErrors.value = false }, 500)
}

const validateStep = (currentStep: number): boolean => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  try {
    if (currentStep === 1) {
      step1Schema.parse(formData)
    } else if (currentStep === 2) {
      step2Schema.parse(formData)
    } else if (currentStep === 3) {
      step3Schema.parse(formData)
    }
    return true
  } catch (err) {
    if (err instanceof z.ZodError) {
      err.errors.forEach(e => {
        if (e.path[0]) {
          errors[e.path[0] as string] = e.message
        }
      })
    }
    triggerShake()
    return false
  }
}

const nextStep = () => {
  if (validateStep(step.value)) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    step.value++
  }
}

const prevStep = () => {
  if (step.value > 1) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    step.value--
  }
}

const submitError = ref('')

const onSubmit = async () => {
  if (!validateStep(3)) return

  isSubmitting.value = true
  submitError.value = ''
  try {
    // Data form dikirim apa adanya ke backend; hasil prediksi yang ditampilkan
    // sepenuhnya berasal dari ML Engine (XGBoost-SGO), bukan perhitungan lokal.
    const response: any = await screeningService.createScreening({ ...formData })
    router.push({ name: 'screening-result', params: { id: response.data.screening_id } })
  } catch (e: any) {
    const serverErrors = e?.response?.data?.errors
    if (serverErrors) {
      // Tampilkan error validasi dari backend pada field terkait
      Object.entries(serverErrors).forEach(([field, messages]: [string, any]) => {
        errors[field] = Array.isArray(messages) ? messages[0] : String(messages)
      })
    }
    submitError.value = e?.response?.data?.message || 'Gagal memproses skrining. Silakan coba lagi.'
    triggerShake()
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  if (route.query.nik) formData.nik = route.query.nik as string
  if (route.query.name) formData.name = route.query.name as string
  if (route.query.dob) formData.date_of_birth = route.query.dob as string
  if (route.query.gender) formData.gender = route.query.gender as string
})
</script>

<style scoped>
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20% { transform: translateX(-8px); }
  40% { transform: translateX(8px); }
  60% { transform: translateX(-8px); }
  80% { transform: translateX(8px); }
}
.animate-shake {
  animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
}

/* Custom styling for standard range inputs */
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 20px;
  width: 20px;
  border-radius: 50%;
  background: #2563eb;
  cursor: pointer;
  margin-top: -8px; /* You need to specify a margin in Chrome, but in Firefox and IE it is automatic */
  box-shadow: 0 0 10px rgba(37,99,235,0.3);
  transition: transform 0.1s;
}

input[type=range]::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

input[type=range]::-webkit-slider-runnable-track {
  width: 100%;
  height: 6px;
  cursor: pointer;
  background: #e2e8f0;
  border-radius: 999px;
}

:global(.dark) input[type=range]::-webkit-slider-runnable-track {
  background: #334155;
}
</style>
