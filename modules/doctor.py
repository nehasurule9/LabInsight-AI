import streamlit as st
import pandas as pd

from modules.database import (
    get_patient,
    search_patients_by_name,
    get_lab_reports
)


# ============================================================
# DOCTOR DASHBOARD
# ============================================================

def doctor_dashboard():

    st.header("👨‍⚕️ Doctor Dashboard")

    st.write(
        "Search for a patient to view complete patient "
        "information, laboratory reports and AI-based "
        "risk predictions."
    )

    # ========================================================
    # SEARCH PATIENT
    # ========================================================

    st.subheader("🔎 Search Patient")

    search_option = st.radio(
        "Search By",
        [
            "Patient ID",
            "Patient Name"
        ],
        horizontal=True
    )

    search_value = st.text_input(
        search_option,
        placeholder=(
            "Enter Patient ID"
            if search_option == "Patient ID"
            else "Enter Patient Name"
        )
    )

    search_button = st.button(
        "🔍 Search Patient",
        use_container_width=True
    )

    # ========================================================
    # SEARCH LOGIC
    # ========================================================

    if search_button:

        if not search_value.strip():

            st.error(
                f"Please enter a {search_option}."
            )

            return

        # ----------------------------------------------------
        # Search by Patient ID
        # ----------------------------------------------------

        if search_option == "Patient ID":

            patient = get_patient(
                search_value.strip()
            )

            if patient is None:

                st.error(
                    "❌ Patient not found. "
                    "Please check the Patient ID."
                )

                return

            st.session_state.doctor_patient = patient

        # ----------------------------------------------------
        # Search by Patient Name
        # ----------------------------------------------------

        else:

            patients = search_patients_by_name(
                search_value
            )

            if len(patients) == 0:

                st.error(
                    "❌ No patient found with that name."
                )

                return

            elif len(patients) == 1:

                st.session_state.doctor_patient = (
                    patients[0]
                )

            else:

                st.warning(
                    f"{len(patients)} patients found. "
                    "Please select the correct patient."
                )

                patient_options = {
                    f"{p[1]} | ID: {p[0]} | Age: {p[2]}": p
                    for p in patients
                }

                selected_patient = st.selectbox(
                    "Select Patient",
                    list(patient_options.keys()),
                    key="doctor_patient_selector"
                )

                st.session_state.doctor_patient = (
                    patient_options[selected_patient]
                )

    # ========================================================
    # NO PATIENT SELECTED
    # ========================================================

    if "doctor_patient" not in st.session_state:

        st.info(
            "Enter a Patient ID or Patient Name above "
            "to view patient information."
        )

        return

    # ========================================================
    # PATIENT INFORMATION
    # ========================================================

    patient = st.session_state.doctor_patient

    patient_id = patient[0]
    patient_name = patient[1]
    patient_age = patient[2]
    phone_number = patient[3]
    gender = patient[4]

    st.divider()

    st.subheader("👤 Patient Information")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Patient ID",
            patient_id
        )

    with col2:

        st.metric(
            "Patient Name",
            patient_name
        )

    with col3:

        st.metric(
            "Age",
            patient_age
            if patient_age is not None
            else "N/A"
        )

    with col4:

        st.metric(
            "Phone Number",
            phone_number
            if phone_number
            else "N/A"
        )

    with col5:

        st.metric(
            "Gender",
            gender
            if gender
            else "N/A"
        )

    # ========================================================
    # GET LAB REPORTS
    # ========================================================

    reports, column_names = get_lab_reports(
        patient_id
    )

    if not reports:

        st.warning(
            "No laboratory reports are available "
            "for this patient."
        )

        return

    df = pd.DataFrame(
        reports,
        columns=column_names
    )

    # Latest report
    latest_report = df.iloc[0]

    # ========================================================
    # LATEST LAB REPORT
    # ========================================================

    st.divider()

    st.subheader(
        "🧪 Latest Laboratory Report"
    )

    report_id = latest_report.get(
        "report_id",
        "N/A"
    )

    created_at = latest_report.get(
        "created_at",
        "N/A"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            f"**Report ID:** {report_id}"
        )

    with col2:

        st.info(
            f"**Report Date:** {created_at}"
        )

    # ========================================================
    # DIABETES REPORT
    # ========================================================

    with st.expander(
        "🩸 Diabetes Laboratory Report",
        expanded=True
    ):

        diabetes_data = {

            "Pregnancies":
                latest_report.get("pregnancies"),

            "Glucose":
                latest_report.get("glucose"),

            "Blood Pressure":
                latest_report.get("blood_pressure"),

            "Skin Thickness":
                latest_report.get("skin_thickness"),

            "Insulin":
                latest_report.get("insulin"),

            "BMI":
                latest_report.get("bmi"),

            "Diabetes Pedigree Function":
                latest_report.get(
                    "diabetes_pedigree"
                ),

            "Age":
                patient_age
        }

        diabetes_df = pd.DataFrame(
            list(diabetes_data.items()),
            columns=[
                "Parameter",
                "Value"
            ]
        )

        st.dataframe(
            diabetes_df,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # KIDNEY REPORT
    # ========================================================

    with st.expander(
        "🫘 Kidney Laboratory Report",
        expanded=True
    ):

        kidney_data = {

            "Age":
                patient_age,

            "Blood Pressure":
                latest_report.get(
                    "blood_pressure"
                ),

            "Specific Gravity":
                latest_report.get(
                    "specific_gravity"
                ),

            "Albumin":
                latest_report.get(
                    "albumin"
                ),

            "Sugar":
                latest_report.get(
                    "sugar"
                ),

            "Red Blood Cells":
                latest_report.get(
                    "red_blood_cells"
                ),

            "Pus Cells":
                latest_report.get(
                    "pus_cells"
                ),

            "Pus Cell Clumps":
                latest_report.get(
                    "pus_cell_clumps"
                ),

            "Bacteria":
                latest_report.get(
                    "bacteria"
                ),

            "Blood Glucose":
                latest_report.get(
                    "blood_glucose"
                ),

            "Blood Urea":
                latest_report.get(
                    "blood_urea"
                ),

            "Creatinine":
                latest_report.get(
                    "creatinine"
                ),

            "Sodium":
                latest_report.get(
                    "sodium"
                ),

            "Potassium":
                latest_report.get(
                    "potassium"
                ),

            "Hemoglobin":
                latest_report.get(
                    "hemoglobin"
                ),

            "Packed Cell Volume":
                latest_report.get(
                    "packed_cell_volume"
                ),

            "White Blood Cell Count":
                latest_report.get(
                    "white_blood_cell_count"
                ),

            "Red Blood Cell Count":
                latest_report.get(
                    "red_blood_cell_count"
                ),

            "Hypertension":
                latest_report.get(
                    "hypertension"
                ),

            "Diabetes Mellitus":
                latest_report.get(
                    "diabetes_mellitus"
                ),

            "Coronary Artery Disease":
                latest_report.get(
                    "coronary_artery_disease"
                ),

            "Appetite":
                latest_report.get(
                    "appetite"
                ),

            "Pedal Edema":
                latest_report.get(
                    "pedal_edema"
                ),

            "Anemia":
                latest_report.get(
                    "anemia"
                )
        }

        kidney_df = pd.DataFrame(
            list(kidney_data.items()),
            columns=[
                "Parameter",
                "Value"
            ]
        )

        st.dataframe(
            kidney_df,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # HEART REPORT
    # ========================================================

    with st.expander(
        "❤️ Heart Laboratory Report",
        expanded=True
    ):

        heart_data = {

            "Age":
                patient_age,

            "Sex":
                latest_report.get(
                    "sex"
                ),

            "Chest Pain Type":
                latest_report.get(
                    "chest_pain_type"
                ),

            "Resting Blood Pressure":
                latest_report.get(
                    "resting_blood_pressure"
                ),

            "Cholesterol":
                latest_report.get(
                    "cholesterol"
                ),

            "Fasting Blood Sugar":
                latest_report.get(
                    "fasting_blood_sugar"
                ),

            "Resting ECG":
                latest_report.get(
                    "resting_ecg"
                ),

            "Maximum Heart Rate":
                latest_report.get(
                    "max_heart_rate"
                ),

            "Exercise Angina":
                latest_report.get(
                    "exercise_angina"
                ),

            "Oldpeak":
                latest_report.get(
                    "oldpeak"
                ),

            "Slope":
                latest_report.get(
                    "slope"
                ),

            "CA":
                latest_report.get(
                    "ca"
                ),

            "Thal":
                latest_report.get(
                    "thal"
                )
        }

        heart_df = pd.DataFrame(
            list(heart_data.items()),
            columns=[
                "Parameter",
                "Value"
            ]
        )

        st.dataframe(
            heart_df,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # AI PREDICTIONS
    # ========================================================

    st.divider()

    st.subheader(
        "🤖 AI Prediction Summary"
    )

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------------
    # Diabetes
    # --------------------------------------------------------

    with col1:

        st.markdown(
            "### 🩸 Diabetes"
        )

        diabetes_prediction = (
            latest_report.get(
                "diabetes_prediction"
            )
        )

        diabetes_confidence = (
            latest_report.get(
                "diabetes_confidence"
            )
        )

        if pd.notna(
            diabetes_prediction
        ):

            st.success(
                str(diabetes_prediction)
            )

            if pd.notna(
                diabetes_confidence
            ):

                st.write(
                    f"Confidence: "
                    f"{float(diabetes_confidence):.2f}%"
                )

        else:

            st.info(
                "No Diabetes prediction available."
            )

    # --------------------------------------------------------
    # Kidney
    # --------------------------------------------------------

    with col2:

        st.markdown(
            "### 🫘 Kidney"
        )

        kidney_prediction = (
            latest_report.get(
                "kidney_prediction"
            )
        )

        kidney_confidence = (
            latest_report.get(
                "kidney_confidence"
            )
        )

        if pd.notna(
            kidney_prediction
        ):

            st.success(
                str(kidney_prediction)
            )

            if pd.notna(
                kidney_confidence
            ):

                st.write(
                    f"Confidence: "
                    f"{float(kidney_confidence):.2f}%"
                )

        else:

            st.info(
                "No Kidney prediction available."
            )

    # --------------------------------------------------------
    # Heart
    # --------------------------------------------------------

    with col3:

        st.markdown(
            "### ❤️ Heart"
        )

        heart_prediction = (
            latest_report.get(
                "heart_prediction"
            )
        )

        heart_confidence = (
            latest_report.get(
                "heart_confidence"
            )
        )

        if pd.notna(
            heart_prediction
        ):

            st.success(
                str(heart_prediction)
            )

            if pd.notna(
                heart_confidence
            ):

                st.write(
                    f"Confidence: "
                    f"{float(heart_confidence):.2f}%"
                )

        else:

            st.info(
                "No Heart prediction available."
            )

    # ========================================================
    # COMPLETE LABORATORY REPORT
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Complete Laboratory Report"
    )

    hidden_columns = [

        "prediction",
        "confidence",

        "diabetes_prediction",
        "diabetes_confidence",

        "kidney_prediction",
        "kidney_confidence",

        "heart_prediction",
        "heart_confidence"
    ]

    display_columns = [
        column
        for column in df.columns
        if column not in hidden_columns
    ]

    complete_report = (
        df[display_columns].copy()
    )

    st.dataframe(
        complete_report,
        use_container_width=True,
        hide_index=True
    )

    # ========================================================
    # PREVIOUS REPORT HISTORY
    # ========================================================

    st.divider()

    st.subheader(
        "📚 Previous Report History"
    )

    if len(df) > 1:

        history_columns = [

            "report_id",
            "created_at",

            "diabetes_prediction",
            "diabetes_confidence",

            "kidney_prediction",
            "kidney_confidence",

            "heart_prediction",
            "heart_confidence"
        ]

        available_columns = [
            column
            for column in history_columns
            if column in df.columns
        ]

        history_df = (
            df[available_columns].copy()
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No previous laboratory reports "
            "are available for this patient."
        )

    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.divider()

    st.caption(
        "⚠️ Disclaimer: AI predictions are "
        "model-based risk indications for "
        "educational/research purposes and "
        "should not be treated as a medical diagnosis."
    )