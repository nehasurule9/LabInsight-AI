import sqlite3
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "labinsight.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    return conn


# ============================================================
# INITIALIZE / MIGRATE DATABASE
# ============================================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Patients table
    # Compatible with your existing database
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            patient_name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            phone_number TEXT
        )
    """)

    # --------------------------------------------------------
    # Lab Reports table
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_reports (

            report_id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id TEXT,

            glucose REAL,
            blood_pressure REAL,
            cholesterol REAL,
            creatinine REAL,
            blood_urea REAL,
            hemoglobin REAL,
            bmi REAL,

            prediction TEXT,
            confidence REAL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            pregnancies REAL,
            skin_thickness REAL,
            insulin REAL,
            diabetes_pedigree REAL,

            specific_gravity REAL,
            albumin REAL,
            sugar REAL,

            red_blood_cells TEXT,
            pus_cells TEXT,
            pus_cell_clumps TEXT,
            bacteria TEXT,

            blood_glucose REAL,
            sodium REAL,
            potassium REAL,
            packed_cell_volume REAL,
            white_blood_cell_count REAL,
            red_blood_cell_count REAL,

            hypertension TEXT,
            diabetes_mellitus TEXT,
            coronary_artery_disease TEXT,
            appetite TEXT,
            pedal_edema TEXT,
            anemia TEXT,

            sex REAL,
            chest_pain_type REAL,
            resting_blood_pressure REAL,
            fasting_blood_sugar REAL,
            resting_ecg REAL,
            max_heart_rate REAL,
            exercise_angina REAL,
            oldpeak REAL,
            slope REAL,
            ca REAL,
            thal REAL,

            diabetes_prediction TEXT,
            diabetes_confidence REAL,

            kidney_prediction TEXT,
            kidney_confidence REAL,

            heart_prediction TEXT,
            heart_confidence REAL
        )
    """)

    conn.commit()

    conn.close()

    migrate_database()


# ============================================================
# DATABASE MIGRATION
# ============================================================

def migrate_database():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------------
    # Check patients columns
    # --------------------------------------------------------

    cursor.execute("PRAGMA table_info(patients)")

    patient_columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    # Add phone_number if missing
    if "phone_number" not in patient_columns:

        cursor.execute("""
            ALTER TABLE patients
            ADD COLUMN phone_number TEXT
        """)

    # --------------------------------------------------------
    # Check lab_reports columns
    # --------------------------------------------------------

    cursor.execute("PRAGMA table_info(lab_reports)")

    report_columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    # --------------------------------------------------------
    # Required columns
    # --------------------------------------------------------

    required_columns = {

        # Diabetes
        "pregnancies": "REAL",
        "skin_thickness": "REAL",
        "insulin": "REAL",
        "diabetes_pedigree": "REAL",

        # Kidney
        "specific_gravity": "REAL",
        "albumin": "REAL",
        "sugar": "REAL",
        "red_blood_cells": "TEXT",
        "pus_cells": "TEXT",
        "pus_cell_clumps": "TEXT",
        "bacteria": "TEXT",
        "blood_glucose": "REAL",
        "sodium": "REAL",
        "potassium": "REAL",
        "packed_cell_volume": "REAL",
        "white_blood_cell_count": "REAL",
        "red_blood_cell_count": "REAL",
        "hypertension": "TEXT",
        "diabetes_mellitus": "TEXT",
        "coronary_artery_disease": "TEXT",
        "appetite": "TEXT",
        "pedal_edema": "TEXT",
        "anemia": "TEXT",

        # Heart
        "sex": "REAL",
        "chest_pain_type": "REAL",
        "resting_blood_pressure": "REAL",
        "fasting_blood_sugar": "REAL",
        "resting_ecg": "REAL",
        "max_heart_rate": "REAL",
        "exercise_angina": "REAL",
        "oldpeak": "REAL",
        "slope": "REAL",
        "ca": "REAL",
        "thal": "REAL",

        # Predictions
        "diabetes_prediction": "TEXT",
        "diabetes_confidence": "REAL",

        "kidney_prediction": "TEXT",
        "kidney_confidence": "REAL",

        "heart_prediction": "TEXT",
        "heart_confidence": "REAL"
    }

    added_columns = 0

    for column_name, column_type in required_columns.items():

        if column_name not in report_columns:

            cursor.execute(
                f"""
                ALTER TABLE lab_reports
                ADD COLUMN {column_name} {column_type}
                """
            )

            added_columns += 1

    conn.commit()

    conn.close()

    print(
        f"Database migration completed. "
        f"Added {added_columns} new columns."
    )


# ============================================================
# ADD / UPDATE PATIENT
# ============================================================

def add_patient(
    patient_id,
    name,
    age=None,
    phone_number=None,
    gender=None
):

    conn = get_connection()
    cursor = conn.cursor()

    # Check if patient already exists
    cursor.execute("""
        SELECT patient_id
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    existing_patient = cursor.fetchone()

    if existing_patient:

        # Update existing patient
        cursor.execute("""
            UPDATE patients
            SET
                patient_name = ?,
                age = ?,
                gender = ?,
                phone = ?,
                phone_number = ?
            WHERE patient_id = ?
        """, (
            name,
            age,
            gender,
            phone_number,
            phone_number,
            patient_id
        ))

    else:

        # Insert new patient
        cursor.execute("""
            INSERT INTO patients
            (
                patient_id,
                patient_name,
                age,
                gender,
                phone,
                phone_number
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            name,
            age,
            gender,
            phone_number,
            phone_number
        ))

    conn.commit()

    conn.close()


# ============================================================
# ADD LABORATORY REPORT
# ============================================================

def add_lab_report(

    patient_id,

    # Common parameters
    glucose=None,
    blood_pressure=None,
    cholesterol=None,
    creatinine=None,
    blood_urea=None,
    hemoglobin=None,
    bmi=None,

    # Diabetes
    pregnancies=None,
    skin_thickness=None,
    insulin=None,
    diabetes_pedigree=None,

    # Kidney
    specific_gravity=None,
    albumin=None,
    sugar=None,
    red_blood_cells=None,
    pus_cells=None,
    pus_cell_clumps=None,
    bacteria=None,
    blood_glucose=None,
    sodium=None,
    potassium=None,
    packed_cell_volume=None,
    white_blood_cell_count=None,
    red_blood_cell_count=None,
    hypertension=None,
    diabetes_mellitus=None,
    coronary_artery_disease=None,
    appetite=None,
    pedal_edema=None,
    anemia=None,

    # Heart
    sex=None,
    chest_pain_type=None,
    resting_blood_pressure=None,
    fasting_blood_sugar=None,
    resting_ecg=None,
    max_heart_rate=None,
    exercise_angina=None,
    oldpeak=None,
    slope=None,
    ca=None,
    thal=None
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lab_reports (

            patient_id,

            glucose,
            blood_pressure,
            cholesterol,
            creatinine,
            blood_urea,
            hemoglobin,
            bmi,

            pregnancies,
            skin_thickness,
            insulin,
            diabetes_pedigree,

            specific_gravity,
            albumin,
            sugar,
            red_blood_cells,
            pus_cells,
            pus_cell_clumps,
            bacteria,

            blood_glucose,
            sodium,
            potassium,
            packed_cell_volume,
            white_blood_cell_count,
            red_blood_cell_count,

            hypertension,
            diabetes_mellitus,
            coronary_artery_disease,
            appetite,
            pedal_edema,
            anemia,

            sex,
            chest_pain_type,
            resting_blood_pressure,
            fasting_blood_sugar,
            resting_ecg,
            max_heart_rate,
            exercise_angina,
            oldpeak,
            slope,
            ca,
            thal
        )

        VALUES (

            ?,

            ?, ?, ?, ?, ?, ?, ?,

            ?, ?, ?, ?,

            ?, ?, ?, ?, ?, ?, ?,

            ?, ?, ?, ?, ?, ?,

            ?, ?, ?, ?, ?, ?,

            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (

        patient_id,

        glucose,
        blood_pressure,
        cholesterol,
        creatinine,
        blood_urea,
        hemoglobin,
        bmi,

        pregnancies,
        skin_thickness,
        insulin,
        diabetes_pedigree,

        specific_gravity,
        albumin,
        sugar,
        red_blood_cells,
        pus_cells,
        pus_cell_clumps,
        bacteria,

        blood_glucose,
        sodium,
        potassium,
        packed_cell_volume,
        white_blood_cell_count,
        red_blood_cell_count,

        hypertension,
        diabetes_mellitus,
        coronary_artery_disease,
        appetite,
        pedal_edema,
        anemia,

        sex,
        chest_pain_type,
        resting_blood_pressure,
        fasting_blood_sugar,
        resting_ecg,
        max_heart_rate,
        exercise_angina,
        oldpeak,
        slope,
        ca,
        thal
    ))

    conn.commit()

    report_id = cursor.lastrowid

    conn.close()

    return report_id


# ============================================================
# GET PATIENT BY ID
# ============================================================

def get_patient(patient_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            patient_name,
            age,
            phone,
            gender
        FROM patients
        WHERE patient_id = ?
    """, (patient_id,))

    patient = cursor.fetchone()

    conn.close()

    return patient


# ============================================================
# GET PATIENT BY NAME
# ============================================================

def search_patients_by_name(patient_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            patient_id,
            patient_name,
            age,
            phone,
            gender
        FROM patients
        WHERE LOWER(patient_name) LIKE LOWER(?)
        ORDER BY patient_name
    """, (
        f"%{patient_name.strip()}%",
    ))

    patients = cursor.fetchall()

    conn.close()

    return patients


# ============================================================
# GET ALL LAB REPORTS FOR PATIENT
# ============================================================

def get_lab_reports(patient_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM lab_reports
        WHERE patient_id = ?
        ORDER BY report_id DESC
    """, (patient_id,))

    reports = cursor.fetchall()

    column_names = [
        description[0]
        for description in cursor.description
    ]

    conn.close()

    return reports, column_names


# ============================================================
# UPDATE DIABETES PREDICTION
# ============================================================

def update_diabetes_prediction(
    patient_id,
    prediction,
    confidence
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lab_reports
        SET
            diabetes_prediction = ?,
            diabetes_confidence = ?
        WHERE report_id = (
            SELECT report_id
            FROM lab_reports
            WHERE patient_id = ?
            ORDER BY report_id DESC
            LIMIT 1
        )
    """, (
        prediction,
        confidence,
        patient_id
    ))

    conn.commit()

    conn.close()


# ============================================================
# UPDATE KIDNEY PREDICTION
# ============================================================

def update_kidney_prediction(
    patient_id,
    prediction,
    confidence
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lab_reports
        SET
            kidney_prediction = ?,
            kidney_confidence = ?
        WHERE report_id = (
            SELECT report_id
            FROM lab_reports
            WHERE patient_id = ?
            ORDER BY report_id DESC
            LIMIT 1
        )
    """, (
        prediction,
        confidence,
        patient_id
    ))

    conn.commit()

    conn.close()


# ============================================================
# UPDATE HEART PREDICTION
# ============================================================

def update_heart_prediction(
    patient_id,
    prediction,
    confidence
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lab_reports
        SET
            heart_prediction = ?,
            heart_confidence = ?
        WHERE report_id = (
            SELECT report_id
            FROM lab_reports
            WHERE patient_id = ?
            ORDER BY report_id DESC
            LIMIT 1
        )
    """, (
        prediction,
        confidence,
        patient_id
    ))

    conn.commit()

    conn.close()


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()