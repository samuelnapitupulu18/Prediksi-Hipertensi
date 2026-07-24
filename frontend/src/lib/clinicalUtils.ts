/**
 * ============================================================================
 *  clinicalUtils.ts — Interpretasi Klinis Deterministik Hipertensi
 * ============================================================================
 *
 *  Referensi Guideline:
 *  - ACC/AHA 2017 (Whelton PK, et al. J Am Coll Cardiol. 2018;71:e127–e248)
 *  - WHO Asia-Pacific BMI Classification
 *  - ESC/ESH 2018 Guidelines for the Management of Arterial Hypertension
 *  - Framingham Heart Study — Simplified 10-Year CVD Risk
 *
 *  ⚠ DISCLAIMER: Fungsi-fungsi ini menghasilkan interpretasi otomatis
 *    berdasarkan guideline medis yang sudah dipublikasi. Hasil interpretasi
 *    BUKAN diagnosis klinis dan harus dikonsultasikan dengan dokter.
 * ============================================================================
 */

// ─── Types ───────────────────────────────────────────────────────────────────

export interface ScreeningData {
  age: number
  gender: string
  bmi: number
  family_history: boolean
  physical_activity: string
  smoking_status: boolean
  red_meat_consumption: string
  salt_consumption: string
  systolic_bp: number
  diastolic_bp: number
}

export interface PredictionData {
  risk_level: 'low' | 'medium' | 'high'
  confidence_score: number
  probability: Record<string, number>
  feature_importance: Array<{ feature: string; importance: number; label: string }>
}

export type BPCategory =
  | 'normal'
  | 'elevated'
  | 'stage1'
  | 'stage2'
  | 'crisis'

export interface BPClassification {
  category: BPCategory
  label: string
  labelEN: string
  color: string
  bgColor: string
  borderColor: string
  darkBgColor: string
  darkBorderColor: string
  description: string
  severity: number // 0-4
}

export type BMICategory =
  | 'underweight'
  | 'normal'
  | 'overweight'
  | 'obese1'
  | 'obese2'
  | 'obese3'

export interface BMIClassification {
  category: BMICategory
  label: string
  range: string
  color: string
  bgColor: string
  borderColor: string
  darkBgColor: string
  darkBorderColor: string
  description: string
  severity: number // 0-5
}

export interface RiskFactor {
  id: string
  label: string
  status: 'high' | 'moderate' | 'normal'
  statusLabel: string
  value: string
  icon: string
  explanation: string
  color: string
  bgColor: string
  borderColor: string
  darkBgColor: string
  darkBorderColor: string
}

export interface Recommendation {
  id: string
  category: string
  title: string
  description: string
  target?: string
  icon: string
  priority: 'critical' | 'important' | 'suggested'
}

export interface FollowUpPlan {
  nextVisit: string
  frequency: string
  additionalTests: string[]
  targetBP: string
  lifestyle: string[]
}

export interface ClinicalConclusion {
  summary: string
  detailedExplanation: string
  bpClassification: BPClassification
  bmiClassification: BMIClassification
  riskFactors: RiskFactor[]
  futureRiskScore: number
  futureRiskLevel: string
  futureRiskExplanation: string
  recommendations: Recommendation[]
  followUpPlan: FollowUpPlan
}

// ─── BP Classification (ACC/AHA 2017) ────────────────────────────────────────

const BP_TABLE: Array<{
  category: BPCategory
  label: string
  labelEN: string
  check: (s: number, d: number) => boolean
  color: string
  bgColor: string
  borderColor: string
  darkBgColor: string
  darkBorderColor: string
  description: string
  severity: number
}> = [
  {
    category: 'crisis',
    label: 'Krisis Hipertensi',
    labelEN: 'Hypertensive Crisis',
    check: (s, d) => s > 180 || d > 120,
    color: 'text-rose-700 dark:text-rose-400',
    bgColor: 'bg-rose-50',
    borderColor: 'border-rose-200',
    darkBgColor: 'dark:bg-rose-950/40',
    darkBorderColor: 'dark:border-rose-800/50',
    description:
      'Tekanan darah sangat tinggi yang memerlukan penanganan medis SEGERA. Kondisi ini dapat menyebabkan kerusakan organ target (otak, jantung, ginjal) dalam hitungan menit hingga jam.',
    severity: 4,
  },
  {
    category: 'stage2',
    label: 'Hipertensi Tahap 2',
    labelEN: 'Stage 2 Hypertension',
    check: (s, d) => s >= 140 || d >= 90,
    color: 'text-red-700 dark:text-red-400',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
    darkBgColor: 'dark:bg-red-950/30',
    darkBorderColor: 'dark:border-red-800/50',
    description:
      'Tekanan darah sudah memasuki tahap hipertensi lanjut. Pada tahap ini, risiko penyakit kardiovaskular (serangan jantung, stroke) meningkat signifikan. Diperlukan perubahan gaya hidup dan evaluasi medis lebih lanjut.',
    severity: 3,
  },
  {
    category: 'stage1',
    label: 'Hipertensi Tahap 1',
    labelEN: 'Stage 1 Hypertension',
    check: (s, d) => s >= 130 || d >= 80,
    color: 'text-orange-700 dark:text-orange-400',
    bgColor: 'bg-orange-50',
    borderColor: 'border-orange-200',
    darkBgColor: 'dark:bg-orange-950/30',
    darkBorderColor: 'dark:border-orange-800/50',
    description:
      'Tekanan darah sudah di atas ambang batas normal. Perubahan gaya hidup seperti diet rendah garam, olahraga teratur, dan manajemen stres sangat dianjurkan. Evaluasi ulang dalam 3-6 bulan.',
    severity: 2,
  },
  {
    category: 'elevated',
    label: 'Tekanan Darah Meningkat',
    labelEN: 'Elevated Blood Pressure',
    check: (s, d) => s >= 120 && d < 80,
    color: 'text-amber-700 dark:text-amber-400',
    bgColor: 'bg-amber-50',
    borderColor: 'border-amber-200',
    darkBgColor: 'dark:bg-amber-950/30',
    darkBorderColor: 'dark:border-amber-800/50',
    description:
      'Tekanan darah sistolik sedikit meningkat namun diastolik masih normal. Tanpa intervensi gaya hidup, kemungkinan besar akan berkembang menjadi hipertensi dalam beberapa tahun.',
    severity: 1,
  },
  {
    category: 'normal',
    label: 'Normal',
    labelEN: 'Normal',
    check: () => true, // fallback
    color: 'text-green-700 dark:text-green-400',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    darkBgColor: 'dark:bg-green-950/30',
    darkBorderColor: 'dark:border-green-800/50',
    description:
      'Tekanan darah dalam rentang normal dan sehat. Pertahankan pola hidup sehat untuk menjaga tekanan darah tetap optimal.',
    severity: 0,
  },
]

export function classifyBloodPressure(
  systolic: number,
  diastolic: number
): BPClassification {
  for (const row of BP_TABLE) {
    if (row.check(systolic, diastolic)) {
      return {
        category: row.category,
        label: row.label,
        labelEN: row.labelEN,
        color: row.color,
        bgColor: row.bgColor,
        borderColor: row.borderColor,
        darkBgColor: row.darkBgColor,
        darkBorderColor: row.darkBorderColor,
        description: row.description,
        severity: row.severity,
      }
    }
  }
  return BP_TABLE[BP_TABLE.length - 1] as BPClassification
}

export const BP_REFERENCE_TABLE = [
  { category: 'Normal', systolic: '< 120', diastolic: '< 80', color: 'green' },
  { category: 'Prehipertensi / Normal Tinggi', systolic: '120 – 139', diastolic: '80 - 89', color: 'amber' },
  { category: 'Hipertensi Tahap 1', systolic: '140 – 159', diastolic: '90 – 99', color: 'orange' },
  { category: 'Hipertensi Tahap 2', systolic: '≥ 160', diastolic: '≥ 100', color: 'red' },
  { category: 'Krisis Hipertensi', systolic: '> 180', diastolic: '> 120', color: 'rose' },
]

export function classifyBMI(bmi: number): BMIClassification {
  if (bmi < 18.5)
    return {
      category: 'underweight',
      label: 'Berat Badan Kurang',
      range: '< 18.5',
      color: 'text-blue-700 dark:text-blue-400',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      darkBgColor: 'dark:bg-blue-950/30',
      darkBorderColor: 'dark:border-blue-800/50',
      description: 'Berat badan di bawah normal. Perlu evaluasi status gizi.',
      severity: 1,
    }
  if (bmi < 23)
    return {
      category: 'normal',
      label: 'Berat Badan Normal',
      range: '18.5 – 22.9',
      color: 'text-green-700 dark:text-green-400',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200',
      darkBgColor: 'dark:bg-green-950/30',
      darkBorderColor: 'dark:border-green-800/50',
      description: 'Indeks massa tubuh dalam rentang sehat. Pertahankan pola makan seimbang.',
      severity: 0,
    }
  if (bmi < 25)
    return {
      category: 'overweight',
      label: 'Kelebihan Berat Badan',
      range: '23.0 – 24.9',
      color: 'text-amber-700 dark:text-amber-400',
      bgColor: 'bg-amber-50',
      borderColor: 'border-amber-200',
      darkBgColor: 'dark:bg-amber-950/30',
      darkBorderColor: 'dark:border-amber-800/50',
      description:
        'Berat badan sedikit berlebih. Peningkatan BMI berkorelasi dengan peningkatan tekanan darah. Disarankan mengurangi asupan kalori dan meningkatkan aktivitas fisik.',
      severity: 2,
    }
  if (bmi < 30)
    return {
      category: 'obese1',
      label: 'Obesitas Tingkat I',
      range: '25.0 – 29.9',
      color: 'text-orange-700 dark:text-orange-400',
      bgColor: 'bg-orange-50',
      borderColor: 'border-orange-200',
      darkBgColor: 'dark:bg-orange-950/30',
      darkBorderColor: 'dark:border-orange-800/50',
      description:
        'Obesitas meningkatkan beban kerja jantung dan resistensi pembuluh darah perifer, yang secara langsung meningkatkan tekanan darah. Setiap penurunan 1 kg berat badan dapat menurunkan TDS sekitar 1 mmHg.',
      severity: 3,
    }
  if (bmi < 35)
    return {
      category: 'obese2',
      label: 'Obesitas Tingkat II',
      range: '30.0 – 34.9',
      color: 'text-red-700 dark:text-red-400',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200',
      darkBgColor: 'dark:bg-red-950/30',
      darkBorderColor: 'dark:border-red-800/50',
      description:
        'Obesitas berat dengan risiko tinggi komplikasi kardiovaskular, yang semuanya memperburuk hipertensi.',
      severity: 4,
    }
  return {
    category: 'obese3',
    label: 'Obesitas Tingkat III (Morbid)',
    range: '≥ 35.0',
    color: 'text-rose-700 dark:text-rose-400',
    bgColor: 'bg-rose-50',
    borderColor: 'border-rose-200',
    darkBgColor: 'dark:bg-rose-950/30',
    darkBorderColor: 'dark:border-rose-800/50',
    description:
      'Obesitas morbid dengan risiko sangat tinggi terhadap hipertensi resisten, gagal jantung, dan mortalitas kardiovaskular.',
    severity: 5,
  }
}

export function analyzeRiskFactors(data: ScreeningData): RiskFactor[] {
  const factors: RiskFactor[] = []

  // 1. Tekanan Darah
  const bp = classifyBloodPressure(data.systolic_bp, data.diastolic_bp)
  factors.push({
    id: 'blood_pressure',
    label: 'Tekanan Darah',
    status: bp.severity >= 3 ? 'high' : bp.severity >= 1 ? 'moderate' : 'normal',
    statusLabel:
      bp.severity >= 3
        ? 'Risiko Tinggi'
        : bp.severity >= 1
          ? 'Perlu Perhatian'
          : 'Normal',
    value: `${data.systolic_bp}/${data.diastolic_bp} mmHg (${bp.label})`,
    icon: '🫀',
    explanation:
      bp.severity >= 2
        ? `Tekanan darah ${data.systolic_bp}/${data.diastolic_bp} mmHg terklasifikasi sebagai "${bp.label}" menurut ACC/AHA 2017. Tekanan darah tinggi yang persisten menyebabkan kerusakan dinding pembuluh darah (aterosklerosis) dan meningkatkan risiko organ.`
        : bp.severity === 1
          ? `Tekanan darah ${data.systolic_bp}/${data.diastolic_bp} mmHg berada di kategori "${bp.label}". Kondisi ini cenderung memburuk seiring waktu tanpa intervensi.`
          : `Tekanan darah ${data.systolic_bp}/${data.diastolic_bp} mmHg dalam rentang normal.`,
    color: bp.severity >= 3 ? 'text-red-700 dark:text-red-400' : bp.severity >= 1 ? 'text-amber-700 dark:text-amber-400' : 'text-green-700 dark:text-green-400',
    bgColor: bp.severity >= 3 ? 'bg-red-50' : bp.severity >= 1 ? 'bg-amber-50' : 'bg-green-50',
    borderColor: bp.severity >= 3 ? 'border-red-200' : bp.severity >= 1 ? 'border-amber-200' : 'border-green-200',
    darkBgColor: bp.severity >= 3 ? 'dark:bg-red-950/30' : bp.severity >= 1 ? 'dark:bg-amber-950/30' : 'dark:bg-green-950/30',
    darkBorderColor: bp.severity >= 3 ? 'dark:border-red-800/50' : bp.severity >= 1 ? 'dark:border-amber-800/50' : 'dark:border-green-800/50',
  })

  // 2. BMI
  const bmiClass = classifyBMI(data.bmi)
  factors.push({
    id: 'bmi',
    label: 'Indeks Massa Tubuh (IMT)',
    status: bmiClass.severity >= 3 ? 'high' : bmiClass.severity >= 2 ? 'moderate' : 'normal',
    statusLabel:
      bmiClass.severity >= 3
        ? 'Risiko Tinggi'
        : bmiClass.severity >= 2
          ? 'Perlu Perhatian'
          : 'Normal',
    value: `${data.bmi.toFixed(1)} kg/m² (${bmiClass.label})`,
    icon: '⚖️',
    explanation: bmiClass.description,
    color: bmiClass.color,
    bgColor: bmiClass.bgColor,
    borderColor: bmiClass.borderColor,
    darkBgColor: bmiClass.darkBgColor,
    darkBorderColor: bmiClass.darkBorderColor,
  })

  // 3. Usia
  const ageRisk = data.age >= 65 ? 'high' : data.age >= 45 ? 'moderate' : 'normal'
  factors.push({
    id: 'age',
    label: 'Usia',
    status: ageRisk as 'high' | 'moderate' | 'normal',
    statusLabel:
      ageRisk === 'high'
        ? 'Risiko Tinggi'
        : ageRisk === 'moderate'
          ? 'Perlu Perhatian'
          : 'Normal',
    value: `${data.age} tahun`,
    icon: '🎂',
    explanation:
      ageRisk === 'high'
        ? `Usia ≥65 tahun merupakan faktor risiko mayor untuk hipertensi akibat perubahan degeneratif pembuluh darah.`
        : ageRisk === 'moderate'
          ? `Usia 45-64 tahun mulai menunjukkan peningkatan prevalensi hipertensi.`
          : `Usia ${data.age} tahun termasuk kategori usia dengan risiko hipertensi yang relatif lebih rendah.`,
    color: ageRisk === 'high' ? 'text-red-700 dark:text-red-400' : ageRisk === 'moderate' ? 'text-amber-700 dark:text-amber-400' : 'text-green-700 dark:text-green-400',
    bgColor: ageRisk === 'high' ? 'bg-red-50' : ageRisk === 'moderate' ? 'bg-amber-50' : 'bg-green-50',
    borderColor: ageRisk === 'high' ? 'border-red-200' : ageRisk === 'moderate' ? 'border-amber-200' : 'border-green-200',
    darkBgColor: ageRisk === 'high' ? 'dark:bg-red-950/30' : ageRisk === 'moderate' ? 'dark:bg-amber-950/30' : 'dark:bg-green-950/30',
    darkBorderColor: ageRisk === 'high' ? 'dark:border-red-800/50' : ageRisk === 'moderate' ? 'dark:border-amber-800/50' : 'dark:border-green-800/50',
  })

  // 4. Riwayat Diabetes
  factors.push({
    id: 'family_history',
    label: 'Riwayat Diabetes Keluarga',
    status: data.family_history ? 'high' : 'normal',
    statusLabel: data.family_history ? 'Ada Riwayat' : 'Tidak Ada',
    value: data.family_history ? 'Ya — Ada riwayat' : 'Tidak ada riwayat',
    icon: '👨‍👩‍👧‍👦',
    explanation: data.family_history
      ? 'Riwayat keluarga dengan diabetes merupakan faktor risiko genetik yang berkontribusi signifikan terhadap hipertensi.'
      : 'Tidak adanya riwayat keluarga diabetes merupakan faktor protektif.',
    color: data.family_history ? 'text-red-700 dark:text-red-400' : 'text-green-700 dark:text-green-400',
    bgColor: data.family_history ? 'bg-red-50' : 'bg-green-50',
    borderColor: data.family_history ? 'border-red-200' : 'border-green-200',
    darkBgColor: data.family_history ? 'dark:bg-red-950/30' : 'dark:bg-green-950/30',
    darkBorderColor: data.family_history ? 'dark:border-red-800/50' : 'dark:border-green-800/50',
  })

  // 5. Merokok
  factors.push({
    id: 'smoking',
    label: 'Status Perokok',
    status: data.smoking_status ? 'high' : 'normal',
    statusLabel: data.smoking_status ? 'Terpapar Asap Rokok' : 'Tidak Merokok',
    value: data.smoking_status ? 'Ya' : 'Tidak',
    icon: '🚬',
    explanation: data.smoking_status
      ? 'Nikotin menyebabkan vasokonstriksi, disfungsi endotel, dan percepatan aterosklerosis. Merokok meningkatkan tekanan darah secara akut.'
      : 'Tidak merokok merupakan faktor protektif yang sangat baik bagi kesehatan kardiovaskular.',
    color: data.smoking_status ? 'text-red-700 dark:text-red-400' : 'text-green-700 dark:text-green-400',
    bgColor: data.smoking_status ? 'bg-red-50' : 'bg-green-50',
    borderColor: data.smoking_status ? 'border-red-200' : 'border-green-200',
    darkBgColor: data.smoking_status ? 'dark:bg-red-950/30' : 'dark:bg-green-950/30',
    darkBorderColor: data.smoking_status ? 'dark:border-red-800/50' : 'dark:border-green-800/50',
  })

  // 6. Aktivitas Fisik
  const activityRisk =
    data.physical_activity === 'low'
      ? 'high'
      : data.physical_activity === 'moderate'
        ? 'moderate'
        : 'normal'
  const activityLabels: Record<string, string> = {
    low: 'Rendah (Kurang Aktif)',
    moderate: 'Sedang',
    high: 'Tinggi (Aktif)',
  }
  factors.push({
    id: 'physical_activity',
    label: 'Aktivitas Fisik',
    status: activityRisk as 'high' | 'moderate' | 'normal',
    statusLabel: activityLabels[data.physical_activity] || data.physical_activity,
    value: activityLabels[data.physical_activity] || data.physical_activity,
    icon: '🏃',
    explanation:
      activityRisk === 'high'
        ? 'Kurangnya aktivitas fisik (sedentari) meningkatkan risiko hipertensi dan obesitas.'
        : activityRisk === 'moderate'
          ? 'Aktivitas fisik sedang memberikan manfaat protektif parsial.'
          : 'Aktivitas fisik tinggi merupakan faktor protektif yang sangat baik.',
    color: activityRisk === 'high' ? 'text-red-700 dark:text-red-400' : activityRisk === 'moderate' ? 'text-amber-700 dark:text-amber-400' : 'text-green-700 dark:text-green-400',
    bgColor: activityRisk === 'high' ? 'bg-red-50' : activityRisk === 'moderate' ? 'bg-amber-50' : 'bg-green-50',
    borderColor: activityRisk === 'high' ? 'border-red-200' : activityRisk === 'moderate' ? 'border-amber-200' : 'border-green-200',
    darkBgColor: activityRisk === 'high' ? 'dark:bg-red-950/30' : activityRisk === 'moderate' ? 'dark:bg-amber-950/30' : 'dark:bg-green-950/30',
    darkBorderColor: activityRisk === 'high' ? 'dark:border-red-800/50' : activityRisk === 'moderate' ? 'dark:border-amber-800/50' : 'dark:border-green-800/50',
  })

  // 7. Konsumsi Daging Merah
  const redMeatRisk = data.red_meat_consumption === 'high' ? 'high' : data.red_meat_consumption === 'moderate' ? 'moderate' : 'normal'
  const redMeatLabels: Record<string, string> = { low: 'Jarang/Tidak', moderate: 'Sedang', high: 'Sering' }
  factors.push({
    id: 'red_meat_consumption',
    label: 'Konsumsi Daging Merah',
    status: redMeatRisk as 'high' | 'moderate' | 'normal',
    statusLabel: redMeatLabels[data.red_meat_consumption] || data.red_meat_consumption,
    value: redMeatLabels[data.red_meat_consumption] || data.red_meat_consumption,
    icon: '🥩',
    explanation: redMeatRisk === 'high'
      ? 'Seringnya asupan lemak jenuh dari daging merah memicu penyempitan pembuluh darah yang dapat meningkatkan tekanan darah.'
      : redMeatRisk === 'moderate'
        ? 'Konsumsi daging merah sesekali masih dalam batas wajar, namun perlu dibatasi.'
        : 'Membatasi daging merah dapat menurunkan asupan lemak jenuh dan menjaga kesehatan kardiovaskular.',
    color: redMeatRisk === 'high' ? 'text-orange-700 dark:text-orange-400' : redMeatRisk === 'moderate' ? 'text-amber-700 dark:text-amber-400' : 'text-green-700 dark:text-green-400',
    bgColor: redMeatRisk === 'high' ? 'bg-orange-50' : redMeatRisk === 'moderate' ? 'bg-amber-50' : 'bg-green-50',
    borderColor: redMeatRisk === 'high' ? 'border-orange-200' : redMeatRisk === 'moderate' ? 'border-amber-200' : 'border-green-200',
    darkBgColor: redMeatRisk === 'high' ? 'dark:bg-orange-950/30' : redMeatRisk === 'moderate' ? 'dark:bg-amber-950/30' : 'dark:bg-green-950/30',
    darkBorderColor: redMeatRisk === 'high' ? 'dark:border-orange-800/50' : redMeatRisk === 'moderate' ? 'dark:border-amber-800/50' : 'dark:border-green-800/50',
  })

  // 8. Konsumsi Garam
  const saltRisk = data.salt_consumption === 'high' ? 'high' : data.salt_consumption === 'moderate' ? 'moderate' : 'normal'
  const saltLabels: Record<string, string> = { low: 'Rendah/Terkontrol', moderate: 'Sedang', high: 'Tinggi/Berlebih' }
  factors.push({
    id: 'salt_consumption',
    label: 'Konsumsi Garam',
    status: saltRisk as 'high' | 'moderate' | 'normal',
    statusLabel: saltLabels[data.salt_consumption] || data.salt_consumption,
    value: saltLabels[data.salt_consumption] || data.salt_consumption,
    icon: '🧂',
    explanation: saltRisk === 'high'
      ? 'Tingginya asupan natrium (garam) akan mengikat cairan di dalam tubuh, meningkatkan volume darah dan secara langsung menaikkan tekanan darah.'
      : saltRisk === 'moderate'
        ? 'Konsumsi garam sedang perlu diawasi untuk mencegah peningkatan tekanan darah.'
        : 'Asupan garam yang terkontrol sangat baik untuk menjaga tekanan darah tetap stabil.',
    color: saltRisk === 'high' ? 'text-red-700 dark:text-red-400' : saltRisk === 'moderate' ? 'text-amber-700 dark:text-amber-400' : 'text-green-700 dark:text-green-400',
    bgColor: saltRisk === 'high' ? 'bg-red-50' : saltRisk === 'moderate' ? 'bg-amber-50' : 'bg-green-50',
    borderColor: saltRisk === 'high' ? 'border-red-200' : saltRisk === 'moderate' ? 'border-amber-200' : 'border-green-200',
    darkBgColor: saltRisk === 'high' ? 'dark:bg-red-950/30' : saltRisk === 'moderate' ? 'dark:bg-amber-950/30' : 'dark:bg-green-950/30',
    darkBorderColor: saltRisk === 'high' ? 'dark:border-red-800/50' : saltRisk === 'moderate' ? 'dark:border-amber-800/50' : 'dark:border-green-800/50',
  })

  return factors
}

export function estimateCardiovascularRisk(
  data: ScreeningData
): { score: number; percentage: number; level: string; explanation: string } {
  let score = 0

  if (data.age >= 65) score += 3
  else if (data.age >= 55) score += 2
  else if (data.age >= 45) score += 1

  if (data.systolic_bp > 180) score += 4
  else if (data.systolic_bp >= 160) score += 3
  else if (data.systolic_bp >= 140) score += 2
  else if (data.systolic_bp >= 130) score += 1

  if (data.bmi >= 30) score += 2
  else if (data.bmi >= 25) score += 1

  if (data.smoking_status) score += 2
  if (data.family_history) score += 1
  if (data.red_meat_consumption !== 'low') score += 1
  if (data.salt_consumption === 'high') score += 2
  else if (data.salt_consumption === 'moderate') score += 1
  if (data.physical_activity === 'high') score -= 1

  score = Math.max(0, score)

  let percentage: number
  let level: string
  let explanation: string

  if (score <= 3) {
    percentage = Math.round(5 + (score / 3) * 5)
    level = 'Rendah'
    explanation = 'Risiko kardiovaskular Anda dalam 10 tahun ke depan tergolong rendah.'
  } else if (score <= 7) {
    percentage = Math.round(10 + ((score - 3) / 4) * 10)
    level = 'Sedang'
    explanation = 'Risiko kardiovaskular Anda dalam 10 tahun ke depan tergolong sedang.'
  } else if (score <= 12) {
    percentage = Math.round(20 + ((score - 7) / 5) * 15)
    level = 'Tinggi'
    explanation = 'Risiko kardiovaskular Anda dalam 10 tahun ke depan tergolong TINGGI. Intervensi sangat dianjurkan.'
  } else {
    percentage = Math.min(50, Math.round(35 + ((score - 12) / 6) * 15))
    level = 'Sangat Tinggi'
    explanation = 'Risiko kardiovaskular Anda dalam 10 tahun ke depan tergolong SANGAT TINGGI.'
  }

  return { score, percentage, level, explanation }
}

export function generateRecommendations(
  data: ScreeningData,
  riskLevel: string
): Recommendation[] {
  const recs: Recommendation[] = []
  const bp = classifyBloodPressure(data.systolic_bp, data.diastolic_bp)
  const bmiClass = classifyBMI(data.bmi)

  if (bp.severity >= 1) {
    recs.push({
      id: 'diet_dash',
      category: 'Pola Makan',
      title: 'Terapkan Pola Diet DASH',
      description: 'Diet DASH terbukti menurunkan tekanan darah. Perbanyak buah, sayuran, dan biji-bijian.',
      target: 'Penurunan TDS: 8-14 mmHg',
      icon: '🥗',
      priority: bp.severity >= 2 ? 'critical' : 'important',
    })
  }

  if (data.salt_consumption !== 'low' || bp.severity >= 1) {
    recs.push({
      id: 'salt_restriction',
      category: 'Pola Makan',
      title: 'Batasi Konsumsi Garam',
      description: 'Kurangi asupan natrium (garam). Hindari makanan olahan dan camilan asin yang mengikat cairan tubuh.',
      target: 'Natrium < 1.500 mg/hari',
      icon: '🧂',
      priority: data.salt_consumption === 'high' ? 'critical' : 'important',
    })
  }

  if (data.red_meat_consumption !== 'low') {
    recs.push({
      id: 'limit_red_meat',
      category: 'Pola Makan',
      title: 'Kurangi Daging Merah',
      description: 'Batasi konsumsi daging merah dan ganti dengan sumber protein rendah lemak (ikan, tahu, tempe).',
      icon: '🥩',
      priority: 'important',
    })
  }

  if (bmiClass.severity >= 2) {
    recs.push({
      id: 'weight_loss',
      category: 'Berat Badan',
      title: 'Penurunan Berat Badan',
      description: `BMI Anda ${data.bmi.toFixed(1)} kg/m². Penurunan berat badan 5-10% sangat efektif menurunkan tekanan darah.`,
      target: 'Target BMI: 18.5-22.9 kg/m²',
      icon: '📉',
      priority: bmiClass.severity >= 3 ? 'critical' : 'important',
    })
  }

  if (data.physical_activity !== 'high') {
    recs.push({
      id: 'exercise',
      category: 'Aktivitas Fisik',
      title: 'Olahraga Aerobik Teratur',
      description: 'Lakukan olahraga sedang (jalan cepat, bersepeda) minimal 150 menit/minggu.',
      target: '150 menit/minggu aerobik',
      icon: '🏃',
      priority: data.physical_activity === 'low' ? 'critical' : 'important',
    })
  }

  if (data.smoking_status) {
    recs.push({
      id: 'quit_smoking',
      category: 'Gaya Hidup',
      title: 'Hindari Asap Rokok',
      description: 'Asap rokok dapat mempercepat kerusakan pembuluh darah. Hindari lingkungan berdebu atau penuh asap rokok.',
      icon: '🚭',
      priority: 'critical',
    })
  }

  if (riskLevel === 'high' || bp.severity >= 3) {
    recs.push({
      id: 'doctor_consultation',
      category: 'Medis',
      title: 'Segera Konsultasi ke Dokter',
      description: 'Anda sangat dianjurkan untuk berkonsultasi dengan dokter untuk evaluasi lanjutan dan pengobatan medis.',
      target: 'Dalam 1-2 minggu',
      icon: '🏥',
      priority: 'critical',
    })
  }

  return recs
}

export function generateFollowUpPlan(
  data: ScreeningData,
  riskLevel: string
): FollowUpPlan {
  const bp = classifyBloodPressure(data.systolic_bp, data.diastolic_bp)

  let nextVisit: string
  let frequency: string

  if (bp.severity >= 4) {
    nextVisit = 'SEGERA — Rujuk ke UGD'
    frequency = 'Setiap hari hingga stabil'
  } else if (bp.severity >= 3 || riskLevel === 'high') {
    nextVisit = '1-2 minggu'
    frequency = 'Setiap 2-4 minggu'
  } else if (bp.severity >= 2 || riskLevel === 'medium') {
    nextVisit = '1-3 bulan'
    frequency = 'Setiap 3-6 bulan'
  } else {
    nextVisit = '6-12 bulan'
    frequency = 'Tahunan'
  }

  const additionalTests: string[] = []

  if (bp.severity >= 2) {
    additionalTests.push('Elektrokardiogram (EKG)')
    additionalTests.push('Fungsi Ginjal (Kreatinin, Urinalisis)')
  }
  if (bp.severity >= 3) {
    additionalTests.push('Ekokardiografi')
  }
  if (data.bmi >= 30) {
    additionalTests.push('Skrining Sleep Apnea')
  }
  if (additionalTests.length === 0) {
    additionalTests.push('Pemeriksaan darah rutin tahunan')
  }

  let targetBP = '< 130/80 mmHg (target umum ACC/AHA 2017)'

  const lifestyle: string[] = [
    'Catat tekanan darah harian',
    'Timbang berat badan'
  ]
  if (data.smoking_status) {
    lifestyle.push('Hindari asap rokok')
  }
  if (data.physical_activity !== 'high') {
    lifestyle.push('Catat durasi olahraga')
  }

  return {
    nextVisit,
    frequency,
    additionalTests,
    targetBP,
    lifestyle,
  }
}

export function generateClinicalConclusion(
  data: ScreeningData,
  prediction: PredictionData
): ClinicalConclusion {
  const bpClass = classifyBloodPressure(data.systolic_bp, data.diastolic_bp)
  const bmiClass = classifyBMI(data.bmi)
  const riskFactors = analyzeRiskFactors(data)
  const cvRisk = estimateCardiovascularRisk(data)
  const recommendations = generateRecommendations(data, prediction.risk_level)
  const followUpPlan = generateFollowUpPlan(data, prediction.risk_level)

  const highRiskCount = riskFactors.filter((f) => f.status === 'high').length
  const moderateRiskCount = riskFactors.filter((f) => f.status === 'moderate').length

  const genderLabel = data.gender === 'male' ? 'Laki-laki' : 'Perempuan'
  let summary = ''

  if (prediction.risk_level === 'high') {
    summary = `Pasien ${genderLabel}, usia ${data.age} tahun, teridentifikasi memiliki RISIKO TINGGI hipertensi berdasarkan analisis model AI (confidence: ${(prediction.confidence_score * 100).toFixed(1)}%). Ditemukan ${highRiskCount} faktor risiko tinggi dan ${moderateRiskCount} faktor risiko sedang. Tekanan darah ${data.systolic_bp}/${data.diastolic_bp} mmHg terklasifikasi sebagai "${bpClass.label}". Diperlukan intervensi segera.`
  } else if (prediction.risk_level === 'medium') {
    summary = `Pasien ${genderLabel}, usia ${data.age} tahun, teridentifikasi memiliki RISIKO SEDANG hipertensi berdasarkan analisis model AI (confidence: ${(prediction.confidence_score * 100).toFixed(1)}%). Ditemukan ${highRiskCount} faktor risiko tinggi dan ${moderateRiskCount} faktor risiko sedang. Tekanan darah ${data.systolic_bp}/${data.diastolic_bp} mmHg terklasifikasi sebagai "${bpClass.label}". Disarankan perubahan gaya hidup dan monitoring.`
  } else {
    summary = `Pasien ${genderLabel}, usia ${data.age} tahun, teridentifikasi memiliki RISIKO RENDAH hipertensi berdasarkan analisis model AI (confidence: ${(prediction.confidence_score * 100).toFixed(1)}%). Tekanan darah ${data.systolic_bp}/${data.diastolic_bp} mmHg terklasifikasi sebagai "${bpClass.label}". Pertahankan gaya hidup sehat.`
  }

  let detailedExplanation = `Hipertensi (tekanan darah tinggi) adalah kondisi kronis dimana tekanan darah di dalam pembuluh arteri secara persisten berada di atas nilai normal. Menurut Pedoman PERKI (Perhimpunan Dokter Spesialis Kardiovaskular Indonesia), tekanan darah dikatakan normal apabila sistolik < 120 mmHg DAN diastolik < 80 mmHg.\n\n`
  detailedExplanation += `Pada pemeriksaan ini, tekanan darah pasien tercatat ${data.systolic_bp}/${data.diastolic_bp} mmHg, yang termasuk dalam kategori "${bpClass.label}" (${bpClass.labelEN}). ${bpClass.description}\n\n`

  if (bpClass.severity >= 2) {
    detailedExplanation += `Hipertensi yang tidak terkontrol dalam jangka panjang dapat menyebabkan komplikasi pada jantung, ginjal, dan otak.\n\n`
  }

  detailedExplanation += `Berdasarkan model prediksi AI, pasien ini memiliki risiko hipertensi tingkat "${prediction.risk_level === 'high' ? 'TINGGI' : prediction.risk_level === 'medium' ? 'SEDANG' : 'RENDAH'}" dengan tingkat keyakinan model sebesar ${(prediction.confidence_score * 100).toFixed(1)}%.`

  return {
    summary,
    detailedExplanation,
    bpClassification: bpClass,
    bmiClassification: bmiClass,
    riskFactors,
    futureRiskScore: cvRisk.percentage,
    futureRiskLevel: cvRisk.level,
    futureRiskExplanation: cvRisk.explanation,
    recommendations,
    followUpPlan,
  }
}
