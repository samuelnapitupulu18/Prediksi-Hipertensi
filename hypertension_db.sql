-- ========================================================
-- SISTEM DETEKSI DINI RISIKO HIPERTENSI
-- COMPLETE DATABASE SCHEMA & DUMMY DATA FOR POSTGRESQL
-- ========================================================

-- Drop tables if they exist to prevent errors on re-import
DROP TABLE IF EXISTS activity_logs CASCADE;
DROP TABLE IF EXISTS predictions CASCADE;
DROP TABLE IF EXISTS screenings CASCADE;
DROP TABLE IF EXISTS patients CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- --------------------------------------------------------
-- Table structure for table `users`
-- --------------------------------------------------------
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    email_verified_at TIMESTAMP NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'perawat',
    remember_token VARCHAR(100) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Default Users
-- Note: Passwords are hashed using standard bcrypt for "password"
INSERT INTO users (name, email, password, role) VALUES 
('Super Administrator', 'admin@hypertension.id', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'super_admin'),
('Dr. Budi Santoso', 'dokter@hypertension.id', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'dokter'),
('Suster Maria', 'perawat@hypertension.id', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'perawat');

-- --------------------------------------------------------
-- Table structure for table `patients`
-- --------------------------------------------------------
CREATE TABLE patients (
    id BIGSERIAL PRIMARY KEY,
    nik VARCHAR(16) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
    phone_number VARCHAR(20) NULL,
    address TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------
-- Table structure for table `screenings`
-- --------------------------------------------------------
CREATE TABLE screenings (
    id BIGSERIAL PRIMARY KEY,
    patient_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
    bmi DOUBLE PRECISION NOT NULL,
    smoking_status VARCHAR(20) NOT NULL CHECK (smoking_status IN ('never', 'former', 'current')),
    alcohol_consumption VARCHAR(20) NOT NULL CHECK (alcohol_consumption IN ('none', 'moderate', 'heavy')),
    physical_activity VARCHAR(20) NOT NULL CHECK (physical_activity IN ('low', 'moderate', 'high')),
    family_history BOOLEAN NOT NULL,
    diabetes BOOLEAN NOT NULL,
    systolic_bp INTEGER NOT NULL,
    diastolic_bp INTEGER NOT NULL,
    cholesterol_level VARCHAR(20) NOT NULL CHECK (cholesterol_level IN ('normal', 'borderline', 'high')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- --------------------------------------------------------
-- Table structure for table `predictions`
-- --------------------------------------------------------
CREATE TABLE predictions (
    id BIGSERIAL PRIMARY KEY,
    screening_id BIGINT NOT NULL,
    risk_level VARCHAR(20) NOT NULL CHECK (risk_level IN ('low', 'medium', 'high')),
    confidence_score DOUBLE PRECISION NOT NULL,
    probability_distribution JSONB NOT NULL,
    feature_importance JSONB NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    inference_time_ms DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (screening_id) REFERENCES screenings(id) ON DELETE CASCADE
);

-- --------------------------------------------------------
-- Table structure for table `activity_logs`
-- --------------------------------------------------------
CREATE TABLE activity_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NULL,
    action VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    context_data JSONB NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- --------------------------------------------------------
-- Dummy Data for `patients`
-- --------------------------------------------------------
INSERT INTO patients (id, nik, name, date_of_birth, gender, phone_number, address) VALUES 
(1, '3171234567890001', 'Budi Harjo', '1975-04-12', 'male', '081234567890', 'Jl. Merdeka No. 1, Jakarta'),
(2, '3171234567890002', 'Siti Aminah', '1982-11-23', 'female', '081298765432', 'Jl. Sudirman No. 45, Bandung'),
(3, '3171234567890003', 'Agus Setiawan', '1968-02-15', 'male', '081312341234', 'Jl. Thamrin No. 9, Surabaya'),
(4, '3171234567890004', 'Rina Marlina', '1990-07-08', 'female', '085612345678', 'Jl. Gatot Subroto No. 22, Medan'),
(5, '3171234567890005', 'Hendra Gunawan', '1955-10-30', 'male', '081198761234', 'Jl. Diponegoro No. 88, Semarang');

-- Adjust the auto-increment sequence for patients
SELECT setval('patients_id_seq', (SELECT MAX(id) FROM patients));

-- --------------------------------------------------------
-- Dummy Data for `screenings`
-- (Assuming user_id 2 is Dokter)
-- --------------------------------------------------------
INSERT INTO screenings (id, patient_id, user_id, age, gender, bmi, smoking_status, alcohol_consumption, physical_activity, family_history, diabetes, systolic_bp, diastolic_bp, cholesterol_level) VALUES 
(1, 1, 2, 49, 'male', 26.5, 'former', 'moderate', 'moderate', true, false, 135, 85, 'borderline'),
(2, 2, 2, 42, 'female', 22.1, 'never', 'none', 'high', false, false, 110, 75, 'normal'),
(3, 3, 2, 56, 'male', 31.2, 'current', 'heavy', 'low', true, true, 160, 100, 'high'),
(4, 4, 2, 34, 'female', 24.8, 'never', 'none', 'moderate', false, false, 120, 80, 'normal'),
(5, 5, 2, 69, 'male', 28.4, 'former', 'none', 'low', true, true, 145, 90, 'high');

-- Adjust the auto-increment sequence for screenings
SELECT setval('screenings_id_seq', (SELECT MAX(id) FROM screenings));

-- --------------------------------------------------------
-- Dummy Data for `predictions`
-- --------------------------------------------------------
INSERT INTO predictions (id, screening_id, risk_level, confidence_score, probability_distribution, feature_importance, model_version, inference_time_ms) VALUES 
(1, 1, 'medium', 0.65, '{"low": 0.2, "medium": 0.65, "high": 0.15}', '[{"feature": "systolic_bp", "importance": 0.3}, {"feature": "bmi", "importance": 0.2}]', 'v1.0.0-sgo', 12.5),
(2, 2, 'low', 0.92, '{"low": 0.92, "medium": 0.05, "high": 0.03}', '[{"feature": "systolic_bp", "importance": 0.25}, {"feature": "age", "importance": 0.2}]', 'v1.0.0-sgo', 10.2),
(3, 3, 'high', 0.88, '{"low": 0.02, "medium": 0.10, "high": 0.88}', '[{"feature": "systolic_bp", "importance": 0.4}, {"feature": "diabetes", "importance": 0.25}]', 'v1.0.0-sgo', 11.1),
(4, 4, 'low', 0.85, '{"low": 0.85, "medium": 0.10, "high": 0.05}', '[{"feature": "age", "importance": 0.22}, {"feature": "systolic_bp", "importance": 0.21}]', 'v1.0.0-sgo', 9.8),
(5, 5, 'high', 0.76, '{"low": 0.04, "medium": 0.20, "high": 0.76}', '[{"feature": "age", "importance": 0.35}, {"feature": "systolic_bp", "importance": 0.3}]', 'v1.0.0-sgo', 13.0);

-- Adjust the auto-increment sequence for predictions
SELECT setval('predictions_id_seq', (SELECT MAX(id) FROM predictions));

-- ========================================================
-- END OF SCRIPT
-- ========================================================
