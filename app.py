import streamlit as st
import joblib
import numpy as np
from PIL import Image
import os

# Set page config first (this must be the very first command)
st.set_page_config(page_title="SWI Prediction", layout="wide", page_icon="🌊")

# Set a more colorful and refined background color scheme
st.markdown("""
    <style>
        .reportview-container {
            background-color: #2f2f2f;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: #2f2f2f;
        }
        .stButton>button {
            background-color: #1E90FF;
            color: white;
            font-size: 18px;
            border-radius: 5px;
        }
        .stTextInput input, .stNumberInput input {
            background-color: #444444;
            color: white;
            font-size: 16px;
            border-radius: 5px;
        }
        h1 {
            font-size: 24px;
            color: #1E90FF;
        }
        .stForm label {
            color: #1E90FF;
            font-size: 16px;
        }
        .stSuccess {
            background-color: #FFFFFF;
            color: white;
        }
        .stWarning {
            background-color: #FFA500;
            color: black;
        }
        .stError {
            background-color: #FF6347;
            color: white;
        }
        .stExpanderHeader {
            color: #FFD700;
        }
    </style>
""", unsafe_allow_html=True)

# Title at the top with a larger font size
st.markdown("<h1 style='text-align: center;'>🌊 Estimating Saltwater Wedge Length in Sloping Coastal Aquifers Using Explainable Machine Learning Models</h1>", unsafe_allow_html=True)

# Developers section (larger font for visibility)
st.markdown("<p style='text-align: center; font-size: 24px; font-weight: bold; color: #FFD700;'>Developers: Mohamed Kamel Elshaarawy & Asaad Mater Armanuos</p>", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 2])

# Left column: Image of the problem
with col1:
    if os.path.exists("sketch.png"):
        image = Image.open("sketch.png")
        image = image.resize((550, 275), Image.LANCZOS)
        st.image(image, use_container_width=True)

# Right column: Input panel and output prediction
with col2:
    # Load model
    @st.cache_resource
    def load_model():
        return joblib.load("XGB.joblib")

    model = load_model()

    # Panel-style for input fields with increased font size
    st.markdown("### Input Parameters (Dimensionless Terms)", unsafe_allow_html=True)

    # Create a form to input values with compact input fields
    with st.form("input_form", clear_on_submit=True):
        with st.expander("Enter Parameters"):
            # Adjust the input fields to fit 6 digits with 6 decimals
            x1 = st.number_input("Relative Density (ρs/ρf):", min_value=0.0, max_value=999999.999999, format="%.6f", help="Enter relative density ratio.")
            x2 = st.number_input("Relative Hydraulic Conductivity (KLo²/Q):", min_value=0.0, max_value=999999.999999, format="%.6f", help="Enter relative hydraulic conductivity ratio.")
            x3 = st.number_input("Bed Slope (tan(β)):", min_value=0.0, max_value=999999.999999, format="%.6f", help="Enter the bed slope (tan(β)).")
            x4 = st.number_input("Relative Head Difference (ΔH/Lo):", min_value=0.0, max_value=999999.999999, format="%.6f", help="Enter the relative head difference.")
            x5 = st.number_input("Relative Recharge Well Distance (Xr/Lo):", min_value=0.0, max_value=999999.999999, format="%.6f", help="Enter the relative recharge well distance.")
            x6 = st.number_input("Relative Recharge Well Depth (Yr/Lo):", min_value=0.0, max_value=999999.999999, format="%.6f", help="Enter the relative recharge well depth.")
            x7 = st.number_input("Relative Recharge Well Rate (Qr/Q):", min_value=0.0, max_value=999999.999999, format="%.6f", help="Enter the relative recharge well rate.")

            submit = st.form_submit_button("Predict 🌊", use_container_width=True)

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
