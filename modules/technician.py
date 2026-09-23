import streamlit as st

from modules.database import (
    add_patient,
    add_lab_report,
    get_patient,
    get_lab_reports,
    update_diabetes_prediction,
    update_kidney_prediction,
    update_heart_prediction
)

from modules.prediction import (
    predict_diabetes,
    predict_kidney,
    predict_heart
)


# ============================================================
# LAB TECHNICIAN DASHBOARD
# ============================================================

def technician_dashboard():

    st.header("🧪 Lab Technician Dashboard")

    # ========================================================
    # SESSION STATE
    # ========================================================

    if "diabetes_result" not in st.session_state:
        st.session_state.diabetes_result = None

    if "diabetes_confidence" not in st.session_state:
        st.session_state.diabetes_confidence = None

    if "kidney_result" not in st.session_state:
        st.session_state.kidney_result = None

    if "kidney_confidence" not in st.session_state:
        st.session_state.kidney_confidence = None

    if "heart_result" not in st.session_state:
        st.session_state.heart_result = None

    if "heart_confidence" not in st.session_state:
        st.session_state.heart_confidence = None

    # ========================================================
    # PATIENT INFORMATION
    # ========================================================

    st.subheader("👤 Patient Information")

    col1, col2 = st.columns(2)

    with col1:

        patient_id = st.text_input(
            "Patient ID",
            placeholder="Example: P001"
        )

    with col2:

        patient_name = st.text_input(
            "Patient Name",
            placeholder="Enter patient name"
        )

    col3, col4, col5 = st.columns(3)

    with col3:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=25,
            step=1
        )

    with col4:

        phone_number = st.text_input(
            "Phone Number",
            placeholder="Enter phone number"
        )

    with col5:

        gender = st.selectbox(
            "Gender",
            [
                "Select Gender",
                "Male",
                "Female",
                "Other"
            ]
        )

    # ========================================================
    # DIABETES TEST
    # ========================================================

    with st.expander("🩸 Diabetes Test", expanded=False):

        st.markdown("### Diabetes Laboratory Parameters")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            pregnancies = st.number_input(
                "Pregnancies",
                min_value=0.0,
                max_value=20.0,
                value=0.0,
                step=1.0
            )

        with col2:

            glucose = st.number_input(
                "Glucose",
                min_value=0.0,
                max_value=300.0,
                value=120.0,
                step=1.0
            )

        with col3:

            blood_pressure = st.number_input(
                "Blood Pressure",
                min_value=0.0,
                max_value=200.0,
                value=70.0,
                step=1.0
            )

        with col4:

            skin_thickness = st.number_input(
                "Skin Thickness",
                min_value=0.0,
                max_value=100.0,
                value=20.0,
                step=1.0
            )

        col5, col6, col7, col8 = st.columns(4)

        with col5:

            insulin = st.number_input(
                "Insulin",
                min_value=0.0,
                max_value=900.0,
                value=80.0,
                step=1.0
            )

        with col6:

            bmi = st.number_input(
                "BMI",
                min_value=0.0,
                max_value=70.0,
                value=25.0,
                step=0.1
            )

        with col7:

            diabetes_pedigree = st.number_input(
                "Diabetes Pedigree Function",
                min_value=0.0,
                max_value=3.0,
                value=0.5,
                step=0.01
            )

        with col8:

            st.write("")
            st.write("")

            predict_diabetes_button = st.button(
                "🔍 Predict Diabetes Risk",
                key="predict_diabetes",
                use_container_width=True
            )

        # ----------------------------------------------------
        # Diabetes Prediction
        # ----------------------------------------------------

        if predict_diabetes_button:

            try:

                result, confidence = predict_diabetes(
                    pregnancies=pregnancies,
                    glucose=glucose,
                    blood_pressure=blood_pressure,
                    skin_thickness=skin_thickness,
                    insulin=insulin,
                    bmi=bmi,
                    diabetes_pedigree=diabetes_pedigree,
                    age=age
                )

                st.session_state.diabetes_result = result
                st.session_state.diabetes_confidence = confidence

                st.success(result)

                st.info(
                    f"Model Confidence: {confidence:.2f}%"
                )

            except Exception as e:

                st.error(
                    f"Diabetes prediction error: {e}"
                )

        # Show previous/current prediction
        if st.session_state.diabetes_result is not None:

            st.markdown("#### Diabetes Prediction")

            st.write(
                st.session_state.diabetes_result
            )

            st.write(
                f"Confidence: "
                f"{st.session_state.diabetes_confidence:.2f}%"
            )

    # ========================================================
    # KIDNEY DISEASE TEST
    # ========================================================

    with st.expander("🫘 Kidney Disease Test", expanded=False):

        st.markdown("### Kidney Laboratory Parameters")

        # ----------------------------------------------------
        # Basic parameters
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            specific_gravity = st.number_input(
                "Specific Gravity",
                min_value=1.000,
                max_value=1.050,
                value=1.020,
                step=0.001,
                format="%.3f"
            )

        with col2:

            albumin = st.number_input(
                "Albumin",
                min_value=0.0,
                max_value=5.0,
                value=0.0,
                step=1.0
            )

        with col3:

            sugar = st.number_input(
                "Sugar",
                min_value=0.0,
                max_value=5.0,
                value=0.0,
                step=1.0
            )

        with col4:

            blood_glucose = st.number_input(
                "Blood Glucose",
                min_value=0.0,
                max_value=500.0,
                value=120.0,
                step=1.0
            )

        # ----------------------------------------------------
        # Blood parameters
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            blood_urea = st.number_input(
                "Blood Urea",
                min_value=0.0,
                max_value=400.0,
                value=40.0,
                step=1.0
            )

        with col2:

            creatinine = st.number_input(
                "Creatinine",
                min_value=0.0,
                max_value=20.0,
                value=1.0,
                step=0.1
            )

        with col3:

            sodium = st.number_input(
                "Sodium",
                min_value=0.0,
                max_value=200.0,
                value=140.0,
                step=1.0
            )

        with col4:

            potassium = st.number_input(
                "Potassium",
                min_value=0.0,
                max_value=15.0,
                value=4.5,
                step=0.1
            )

        # ----------------------------------------------------
        # Blood cell parameters
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            hemoglobin = st.number_input(
                "Hemoglobin",
                min_value=0.0,
                max_value=30.0,
                value=14.0,
                step=0.1
            )

        with col2:

            packed_cell_volume = st.number_input(
                "Packed Cell Volume",
                min_value=0.0,
                max_value=70.0,
                value=40.0,
                step=1.0
            )

        with col3:

            white_blood_cell_count = st.number_input(
                "White Blood Cell Count",
                min_value=0.0,
                max_value=30000.0,
                value=8000.0,
                step=100.0
            )

        with col4:

            red_blood_cell_count = st.number_input(
                "Red Blood Cell Count",
                min_value=0.0,
                max_value=10.0,
                value=5.0,
                step=0.1
            )

        # ----------------------------------------------------
        # Kidney categorical parameters
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            red_blood_cells = st.selectbox(
                "Red Blood Cells",
                [
                    "normal",
                    "abnormal"
                ],
                key="kidney_rbc"
            )

        with col2:

            pus_cells = st.selectbox(
                "Pus Cells",
                [
                    "normal",
                    "abnormal"
                ],
                key="kidney_pc"
            )

        with col3:

            pus_cell_clumps = st.selectbox(
                "Pus Cell Clumps",
                [
                    "notpresent",
                    "present"
                ],
                key="kidney_pcc"
            )

        with col4:

            bacteria = st.selectbox(
                "Bacteria",
                [
                    "notpresent",
                    "present"
                ],
                key="kidney_ba"
            )

        # ----------------------------------------------------
        # Medical history
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            hypertension = st.selectbox(
                "Hypertension",
                [
                    "no",
                    "yes"
                ],
                key="kidney_htn"
            )

        with col2:

            diabetes_mellitus = st.selectbox(
                "Diabetes Mellitus",
                [
                    "no",
                    "yes"
                ],
                key="kidney_dm"
            )

        with col3:

            coronary_artery_disease = st.selectbox(
                "Coronary Artery Disease",
                [
                    "no",
                    "yes"
                ],
                key="kidney_cad"
            )

        with col4:

            appetite = st.selectbox(
                "Appetite",
                [
                    "good",
                    "poor"
                ],
                key="kidney_appet"
            )

        # ----------------------------------------------------
        # Additional parameters
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            pedal_edema = st.selectbox(
                "Pedal Edema",
                [
                    "no",
                    "yes"
                ],
                key="kidney_pe"
            )

        with col2:

            anemia = st.selectbox(
                "Anemia",
                [
                    "no",
                    "yes"
                ],
                key="kidney_ane"
            )

        with col3:

            predict_kidney_button = st.button(
                "🔍 Predict Kidney Risk",
                key="predict_kidney",
                use_container_width=True
            )

        # ----------------------------------------------------
        # Kidney Prediction
        # ----------------------------------------------------

        if predict_kidney_button:

            try:

                result, confidence = predict_kidney(

                    age=age,

                    blood_pressure=blood_pressure,

                    specific_gravity=specific_gravity,

                    albumin=albumin,

                    sugar=sugar,

                    red_blood_cells=red_blood_cells,

                    pus_cells=pus_cells,

                    pus_cell_clumps=pus_cell_clumps,

                    bacteria=bacteria,

                    blood_glucose=blood_glucose,

                    blood_urea=blood_urea,

                    creatinine=creatinine,

                    sodium=sodium,

                    potassium=potassium,

                    hemoglobin=hemoglobin,

                    packed_cell_volume=packed_cell_volume,

                    white_blood_cell_count=white_blood_cell_count,

                    red_blood_cell_count=red_blood_cell_count,

                    hypertension=hypertension,

                    diabetes_mellitus=diabetes_mellitus,

                    coronary_artery_disease=coronary_artery_disease,

                    appetite=appetite,

                    pedal_edema=pedal_edema,

                    anemia=anemia
                )

                st.session_state.kidney_result = result

                st.session_state.kidney_confidence = confidence

                st.success(result)

                st.info(
                    f"Model Confidence: {confidence:.2f}%"
                )

            except Exception as e:

                st.error(
                    f"Kidney prediction error: {e}"
                )

        # Show current prediction

        if st.session_state.kidney_result is not None:

            st.markdown("#### Kidney Prediction")

            st.write(
                st.session_state.kidney_result
            )

            st.write(
                f"Confidence: "
                f"{st.session_state.kidney_confidence:.2f}%"
            )

    # ========================================================
    # HEART DISEASE TEST
    # ========================================================

    with st.expander("❤️ Heart Disease Test", expanded=False):

        st.markdown("### Heart Laboratory Parameters")

        # ----------------------------------------------------
        # Heart parameters
        # ----------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            sex = st.selectbox(
                "Sex",
                [
                    1,
                    0
                ],
                format_func=lambda x:
                    "Male" if x == 1 else "Female",
                key="heart_sex"
            )

        with col2:

            chest_pain_type = st.selectbox(
                "Chest Pain Type",
                [0, 1, 2, 3],
                key="heart_cp"
            )

        with col3:

            resting_blood_pressure = st.number_input(
                "Resting Blood Pressure",
                min_value=0.0,
                max_value=250.0,
                value=120.0,
                step=1.0
            )

        with col4:

            cholesterol = st.number_input(
                "Cholesterol",
                min_value=0.0,
                max_value=700.0,
                value=200.0,
                step=1.0
            )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            fasting_blood_sugar = st.selectbox(
                "Fasting Blood Sugar",
                [0, 1],
                key="heart_fbs"
            )

        with col2:

            resting_ecg = st.selectbox(
                "Resting ECG",
                [0, 1, 2],
                key="heart_ecg"
            )

        with col3:

            max_heart_rate = st.number_input(
                "Maximum Heart Rate",
                min_value=0.0,
                max_value=250.0,
                value=150.0,
                step=1.0
            )

        with col4:

            exercise_angina = st.selectbox(
                "Exercise Angina",
                [0, 1],
                key="heart_exang"
            )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            oldpeak = st.number_input(
                "Oldpeak",
                min_value=0.0,
                max_value=10.0,
                value=1.0,
                step=0.1
            )

        with col2:

            slope = st.selectbox(
                "Slope",
                [0, 1, 2],
                key="heart_slope"
            )

        with col3:

            ca = st.selectbox(
                "CA",
                [0, 1, 2, 3, 4],
                key="heart_ca"
            )

        with col4:

            thal = st.selectbox(
                "Thal",
                [0, 1, 2, 3],
                key="heart_thal"
            )

        # ----------------------------------------------------
        # Heart prediction button
        # ----------------------------------------------------

        predict_heart_button = st.button(
            "🔍 Predict Heart Disease Risk",
            key="predict_heart",
            use_container_width=True
        )

        # ----------------------------------------------------
        # Heart Prediction
        # ----------------------------------------------------

        if predict_heart_button:

            try:

                result, confidence = predict_heart(

                    age=age,

                    sex=sex,

                    chest_pain_type=chest_pain_type,

                    resting_blood_pressure=resting_blood_pressure,

                    cholesterol=cholesterol,

                    fasting_blood_sugar=fasting_blood_sugar,

                    resting_ecg=resting_ecg,

                    max_heart_rate=max_heart_rate,

                    exercise_angina=exercise_angina,

                    oldpeak=oldpeak,

                    slope=slope,

                    ca=ca,

                    thal=thal
                )

                st.session_state.heart_result = result

                st.session_state.heart_confidence = confidence

                st.success(result)

                st.info(
                    f"Model Confidence: {confidence:.2f}%"
                )

            except Exception as e:

                st.error(
                    f"Heart prediction error: {e}"
                )

        # Show current prediction

        if st.session_state.heart_result is not None:

            st.markdown("#### Heart Prediction")

            st.write(
                st.session_state.heart_result
            )

            st.write(
                f"Confidence: "
                f"{st.session_state.heart_confidence:.2f}%"
            )

    # ========================================================
    # CURRENT AI PREDICTIONS
    # ========================================================

    st.subheader("📊 Current AI Predictions")

    col1, col2, col3 = st.columns(3)

    # --------------------------------------------------------
    # Diabetes
    # --------------------------------------------------------

    with col1:

        st.markdown("### 🩸 Diabetes")

        if st.session_state.diabetes_result is not None:

            st.success(
                st.session_state.diabetes_result
            )

            st.write(
                f"Confidence: "
                f"{st.session_state.diabetes_confidence:.2f}%"
            )

        else:

            st.info("Not predicted yet")

    # --------------------------------------------------------
    # Kidney
    # --------------------------------------------------------

    with col2:

        st.markdown("### 🫘 Kidney")

        if st.session_state.kidney_result is not None:

            st.success(
                st.session_state.kidney_result
            )

            st.write(
                f"Confidence: "
                f"{st.session_state.kidney_confidence:.2f}%"
            )

        else:

            st.info("Not predicted yet")

    # --------------------------------------------------------
    # Heart
    # --------------------------------------------------------

    with col3:

        st.markdown("### ❤️ Heart")

        if st.session_state.heart_result is not None:

            st.success(
                st.session_state.heart_result
            )

            st.write(
                f"Confidence: "
                f"{st.session_state.heart_confidence:.2f}%"
            )

        else:

            st.info("Not predicted yet")

    # ========================================================
    # SAVE COMPLETE LABORATORY REPORT
    # ========================================================

    st.divider()

    if st.button(
        "💾 Save Complete Laboratory Report",
        use_container_width=True
    ):

        # ----------------------------------------------------
        # Basic validation
        # ----------------------------------------------------

        if not patient_id.strip():

            st.error("Please enter Patient ID.")

            return

        if not patient_name.strip():

            st.error("Please enter Patient Name.")

            return

        # ----------------------------------------------------
        # Gender
        # ----------------------------------------------------

        if gender == "Select Gender":

            gender_value = None

        else:

            gender_value = gender

        # ----------------------------------------------------
        # Save / update patient
        # ----------------------------------------------------

        try:

            add_patient(
                patient_id=patient_id,
                name=patient_name,
                age=age,
                phone_number=phone_number,
                gender=gender_value
            )

            # ------------------------------------------------
            # Save laboratory report
            # ------------------------------------------------

            report_id = add_lab_report(

                patient_id=patient_id,

                # Basic values
                glucose=glucose,
                blood_pressure=blood_pressure,
                cholesterol=cholesterol,
                creatinine=creatinine,
                blood_urea=blood_urea,
                hemoglobin=hemoglobin,
                bmi=bmi,

                # Diabetes
                pregnancies=pregnancies,
                skin_thickness=skin_thickness,
                insulin=insulin,
                diabetes_pedigree=diabetes_pedigree,

                # Kidney
                specific_gravity=specific_gravity,
                albumin=albumin,
                sugar=sugar,
                red_blood_cells=red_blood_cells,
                pus_cells=pus_cells,
                pus_cell_clumps=pus_cell_clumps,
                bacteria=bacteria,

                blood_glucose=blood_glucose,
                sodium=sodium,
                potassium=potassium,
                packed_cell_volume=packed_cell_volume,
                white_blood_cell_count=white_blood_cell_count,
                red_blood_cell_count=red_blood_cell_count,

                hypertension=hypertension,
                diabetes_mellitus=diabetes_mellitus,
                coronary_artery_disease=coronary_artery_disease,
                appetite=appetite,
                pedal_edema=pedal_edema,
                anemia=anemia,

                # Heart
                sex=sex,
                chest_pain_type=chest_pain_type,
                resting_blood_pressure=resting_blood_pressure,
                fasting_blood_sugar=fasting_blood_sugar,
                resting_ecg=resting_ecg,
                max_heart_rate=max_heart_rate,
                exercise_angina=exercise_angina,
                oldpeak=oldpeak,
                slope=slope,
                ca=ca,
                thal=thal
            )

            # ------------------------------------------------
            # Save Diabetes Prediction
            # ------------------------------------------------

            if st.session_state.diabetes_result is not None:

                update_diabetes_prediction(
                    patient_id=patient_id,
                    prediction=st.session_state.diabetes_result,
                    confidence=st.session_state.diabetes_confidence
                )

            # ------------------------------------------------
            # Save Kidney Prediction
            # ------------------------------------------------

            if st.session_state.kidney_result is not None:

                update_kidney_prediction(
                    patient_id=patient_id,
                    prediction=st.session_state.kidney_result,
                    confidence=st.session_state.kidney_confidence
                )

            # ------------------------------------------------
            # Save Heart Prediction
            # ------------------------------------------------

            if st.session_state.heart_result is not None:

                update_heart_prediction(
                    patient_id=patient_id,
                    prediction=st.session_state.heart_result,
                    confidence=st.session_state.heart_confidence
                )

            # ------------------------------------------------
            # Success message
            # ------------------------------------------------

            st.success(
                f"✅ Laboratory Report #{report_id} "
                f"saved successfully!"
            )

            st.info(
                "Patient information and AI predictions "
                "have been saved to the database."
            )

        except Exception as e:

            st.error(
                f"Error saving laboratory report: {e}"
            )

    # ========================================================
    # DISCLAIMER
    # ========================================================

    st.divider()

    st.caption(
        "⚠️ Disclaimer: AI predictions are model-based "
        "risk indications for educational/research purposes "
        "and should not be treated as a medical diagnosis."
    )