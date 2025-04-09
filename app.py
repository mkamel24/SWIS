import streamlit as st
import joblib
import os
from PIL import Image

# Load the model
model_path = os.path.join(os.path.dirname(__file__), "XGB.joblib")
if not os.path.exists(model_path):
    st.error("Model file not found. Please ensure XGB.joblib is in the same directory as this app.")
    st.stop()

model = joblib.load(model_path)

# Load image if it exists
image_path = os.path.join(os.path.dirname(__file__), "sketch.png")
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.image(image, caption="Conceptual Sketch", use_column_width=True)

# App title and authors
st.title("Estimating Saltwater Wedge Length in Sloping Coastal Aquifers")
st.markdown("**Using Explainable Machine Learning Models**")
st.markdown("**Developers: Mohamed Kamel Elshaarawy & Asaad Mater Armanuos**")

# Input form
st.markdown("### Input Parameters (Dimensionless Terms)")

x1 = st.number_input("Relative Density (ρs/ρf)", min_value=0.0, format="%.5f")
x2 = st.number_input("Relative Hydraulic Conductivity (KLo²/Q)", min_value=0.0, format="%.5f")
x3 = st.number_input("Bed Slope (tan(β))", min_value=0.0, format="%.5f")
x4 = st.number_input("Relative Head Difference (ΔH/Lo)", min_value=0.0, format="%.5f")
x5 = st.number_input("Relative Recharge Well Distance (Xr/Lo)", min_value=0.0, format="%.5f")
x6 = st.number_input("Relative Recharge Well Depth (Yr/Lo)", min_value=0.0, format="%.5f")
x7 = st.number_input("Relative Recharge Well Rate (Qr/Q)", min_value=0.0, format="%.5f")

# Prediction
if st.button("Predict"):
    try:
        input_data = [[x1, x2, x3, x4, x5, x6, x7]]
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted SWI Wedge Length Ratio (L/Lo): **{prediction:.4f}**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
