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

# Load and resize image
image_path = os.path.join(os.path.dirname(__file__), "sketch.png")
if os.path.exists(image_path):
    image = Image.open(image_path)
    scale_ratio = 0.6  # Adjust this between 0.1 to 1.0 as needed
    new_size = (int(image.width * scale_ratio), int(image.height * scale_ratio))
    resized_image = image.resize(new_size)
    st.image(resized_image, caption="Conceptual Sketch")

# Custom fonts and title using HTML/CSS
st.markdown("""
    <h2 style='text-align: center; font-family: Georgia, serif; color: #2F4F4F;'>
        Estimating Saltwater Wedge Length in Sloping Coastal Aquifers
    </h2>
    <p style='text-align: center; font-size:16px; font-family:Courier New; color: #555;'>
        <strong>Using Explainable Machine Learning Models</strong><br>
        Developers: <em>Mohamed Kamel Elshaarawy & Asaad Mater Armanuos</em>
    </p>
""", unsafe_allow_html=True)

# Input form
st.markdown("<h4 style='font-family:Verdana; color:#003366;'>Input Parameters (Dimensionless Terms)</h4>", unsafe_allow_html=True)

# Compact inputs
col1, col2 = st.columns(2)

with col1:
    x1 = st.number_input("Relative Density (ρs/ρf)", min_value=0.0, format="%.5f", key="x1")
    x2 = st.number_input("Hydraulic Conductivity Ratio (KLo²/Q)", min_value=0.0, format="%.5f", key="x2")
    x3 = st.number_input("Bed Slope (tan(β))", min_value=0.0, format="%.5f", key="x3")

with col2:
    x4 = st.number_input("Head Difference Ratio (ΔH/Lo)", min_value=0.0, format="%.5f", key="x4")
    x5 = st.number_input("Relative Recharge Well Distance Ratio (Xr/Lo)", min_value=0.0, format="%.5f", key="x5")
    x6 = st.number_input("Relative Recharge Well Depth Ratio (Yr/Lo)", min_value=0.0, format="%.5f", key="x6")
    x7 = st.number_input("Relative Recharge Well Rate Ratio (Qr/Q)", min_value=0.0, format="%.5f", key="x7")

# Prediction
if st.button("Predict"):
    if all(v == 0.0 for v in [x1, x2, x3, x4, x5, x6, x7]):
        st.warning("Please enter non-zero values for at least one input to make a prediction.")
    else:
        try:
            input_data = [[x1, x2, x3, x4, x5, x6, x7]]
            prediction = model.predict(input_data)[0]
            st.success(f"Predicted SWI Wedge Length Ratio (L/Lo): **{prediction:.4f}**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
