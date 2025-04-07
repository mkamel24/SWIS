import streamlit as st
import joblib
import numpy as np
from PIL import Image
import os

# Title and image
st.set_page_config(page_title="SWI Prediction", layout="centered")
st.markdown("<h1 style='text-align: center; color: white;'>Gradient Boosting-Based Modeling of Seawater Intrusion</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>in Sloping Coastal Aquifers</h3>", unsafe_allow_html=True)

# Load image
if os.path.exists("sketch.png"):
    image = Image.open("sketch.png")
    st.image(image, use_container_width=True)

# Developer credit
st.markdown("<p style='text-align: center; font-weight: bold; color: white;'>Developers: Mohamed Kamel Elshaarawy & Asaad Mater Armanuos</p>", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return joblib.load("CGB.joblib")

model = load_model()

# Input form
st.markdown("### Input Parameters (Dimensionless Terms)")
with st.form("input_form"):
    col1, col2 = st.columns(2)

    x1 = col1.number_input("Relative Density (ρs/ρf):", min_value=0.0, format="%.4f")
    x2 = col2.number_input("Relative Hydraulic Conductivity (KLo²/Q):", min_value=0.0, format="%.4f")
    x3 = col1.number_input("Bed Slope (tan(β)):", min_value=0.0, format="%.4f")
    x4 = col2.number_input("Relative Head Difference (i/Lo):", min_value=0.0, format="%.4f")
    x5 = col1.number_input("Recharge Well Distance (Xr/Lo):", min_value=0.0, format="%.4f")
    x6 = col2.number_input("Recharge Well Depth (Yr/Lo):", min_value=0.0, format="%.4f")
    x7 = col1.number_input("Recharge Well Rate (Qr/Q):", min_value=0.0, format="%.4f")

    submit = st.form_submit_button("Predict")

# Predict and display output
if submit:
    try:
        inputs = np.array([[x1, x2, x3, x4, x5, x6, x7]])
        prediction = model.predict(inputs)[0]
        st.success(f"🔍 Predicted SWI Wedge Length Ratio (L/Lo): **{prediction:.4f}**")
    except Exception as e:
        st.error(f"❌ Prediction Error: {e}")
