CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    patient_name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lab_reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,

    patient_id TEXT,

    glucose REAL,
    blood_pressure REAL,
    cholesterol REAL,
    creatinine REAL,
    blood_urea REAL,
    hemoglobin REAL,
    n

     
    bmi REAL,

    prediction TEXT,
    confidence REAL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(patient_id)
    REFERENCES patients(patient_id)
);