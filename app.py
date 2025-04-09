import streamlit as st
import joblib
import numpy as np
from PIL import Image
import os

# Title and image
st.set_page_config(page_title="SWI Prediction", layout="centered", page_icon="🌊")
st.markdown("<h1 style='text-align: center; color: #1E90FF;'>Gradient Boosting-Based Modeling of Seawater Intrusion</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: white;'>in Sloping Coastal Aquifers</h3>", unsafe_allow_html=True)

# Image on the right
col1, col2 = st.columns([2, 3])  # Increase the right column's width to give space for the image
with col2:
    if os.path.exists("sketch.png"):
        image = Image.open("sketch.png")
        st.image(image, use_container_width=True)

# Developer credit with highlighting
with col1:
    st.markdown("<p style='text-align: center; font-size: 20px; font-weight: bold; color: #FFD700;'>Developers: Mohamed Kamel Elshaarawy & Asaad Mater Armanuos</p>", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return joblib.load("CGB.joblib")

model = load_model()

# Input form with modern style
st.markdown("### Input Parameters (Dimensionless Terms)", unsafe_allow_html=True)
with st.form("input_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    x1 = col1.number_input("Relative Density (ρs/ρf):", min_value=0.0, format="%.4f", step=0.0001, help="Enter relative density ratio.")
    x2 = col2.number_input("Relative Hydraulic Conductivity (KLo²/Q):", min_value=0.0, format="%.4f", step=0.0001, help="Enter relative hydraulic conductivity ratio.")
    x3 = col1.number_input("Bed Slope (tan(β)):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the bed slope (tan(β)).")
    x4 = col2.number_input("Relative Head Difference (i/Lo):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the relative head difference.")
    x5 = col1.number_input("Recharge Well Distance (Xr/Lo):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the recharge well distance.")
    x6 = col2.number_input("Recharge Well Depth (Yr/Lo):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the recharge well depth.")
    x7 = col1.number_input("Recharge Well Rate (Qr/Q):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the recharge well rate.")

    submit = st.form_submit_button("Predict", use_container_width=True)

# Predict and display output
if submit:
    # Check if all inputs are zero
    if all(val == 0.0 for val in [x1, x2, x3, x4, x5, x6, x7]):
        st.warning("⚠️ Please enter valid values for the parameters. All inputs cannot be zero as it will produce an invalid prediction.")
    else:
        try:
            inputs = np.array([[x1, x2, x3, x4, x5, x6, x7]])
            prediction = model.predict(inputs)[0]
            st.success(f"🔍 Predicted SWI Wedge Length Ratio (L/Lo): **{prediction:.4f}**")
        except Exception as e:
            st.error(f"❌ Prediction Error: {e}")
