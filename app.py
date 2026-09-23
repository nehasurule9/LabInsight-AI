import streamlit as st
from modules.technician import technician_dashboard
from modules.doctor import doctor_dashboard

st.set_page_config(
    page_title="LabInsight AI",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 LabInsight AI")
st.subheader("Medical Laboratory Data Analysis and Disease Prediction")

page = st.sidebar.radio(
    "Select Dashboard",
    ["Lab Technician", "Doctor"]
)

if page == "Lab Technician":
    technician_dashboard()
else:
    doctor_dashboard()