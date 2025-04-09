import streamlit as st
import joblib
import numpy as np
from PIL import Image
import os

# Set page config first (this must be the very first command)
st.set_page_config(page_title="SWI Prediction", layout="wide", page_icon="🌊")

# Set a light background color for the app
st.markdown("""
    <style>
        .reportview-container {
            background-color: #000000;
        }
        .sidebar .sidebar-content {
            background-color: #000000;
        }
        .stButton>button {
            background-color: #000000;
            color: white;
            font-size: 18px;
        }
        .stTextInput input {
            font-size: 18px;
        }
        .stNumberInput input {
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 2])

# Left side content: Title, developer info, and image
with col1:
    st.markdown("<h1 style='text-align: center; color: #1E90FF; font-size: 28px;'>Estimating Saltwater Wedge Length in Sloping Coastal Aquifers Using Explainable Machine Learning Models</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: left; font-size: 20px; font-weight: bold; color: #FFD700;'>Developers: Mohamed Kamel Elshaarawy & Asaad Mater Armanuos</p>", unsafe_allow_html=True)
    
    # Load and display the image
    if os.path.exists("sketch.png"):
        image = Image.open("sketch.png")
        image = image.resize((600, 400), Image.LANCZOS)
        st.image(image, use_container_width=True)

# Right side content: Input panel and output prediction
with col2:
    # Load model
    @st.cache_resource
    def load_model():
        return joblib.load("XGB.joblib")

    model = load_model()

    # Panel-style for input fields with increased font size
    st.markdown("### Input Parameters (Dimensionless Terms)", unsafe_allow_html=True)

    # Create a form to input values
    with st.form("input_form", clear_on_submit=True):
        with st.expander("Enter Parameters"):
            # Arrange inputs vertically in the form
            x1 = st.number_input("Relative Density (ρs/ρf):", min_value=0.0, format="%.4f", step=0.0001, help="Enter relative density ratio.")
            x2 = st.number_input("Relative Hydraulic Conductivity (KLo²/Q):", min_value=0.0, format="%.4f", step=0.0001, help="Enter relative hydraulic conductivity ratio.")
            x3 = st.number_input("Bed Slope (tan(β)):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the bed slope (tan(β)).")
            x4 = st.number_input("Relative Head Difference (ΔH/Lo):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the relative head difference.")
            x5 = st.number_input("Relative Recharge Well Distance (Xr/Lo):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the relative recharge well distance.")
            x6 = st.number_input("Relative Recharge Well Depth (Yr/Lo):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the relative recharge well depth.")
            x7 = st.number_input("Relative Recharge Well Rate (Qr/Q):", min_value=0.0, format="%.4f", step=0.0001, help="Enter the relative recharge well rate.")

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
