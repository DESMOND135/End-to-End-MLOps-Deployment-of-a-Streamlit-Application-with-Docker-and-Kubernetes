import streamlit as st
import joblib
import numpy as np
import os

# ─── Configuration ─────────────────────────────────────────────────────────────
MODEL_DIR = os.getcwd()   # assumes all .joblib files are in the project root

# ─── Load artifacts ────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model = joblib.load(os.path.join(MODEL_DIR, "model.joblib"))
    scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.joblib"))
    sex_encoder = joblib.load(os.path.join(MODEL_DIR, "sex_encoder.joblib"))
    smoker_encoder = joblib.load(os.path.join(MODEL_DIR, "smoker_encoder.joblib"))
    region_encoder = joblib.load(os.path.join(MODEL_DIR, "region_encoder.joblib"))
    return model, scaler, sex_encoder, smoker_encoder, region_encoder

try:
    model, scaler, sex_encoder, smoker_encoder, region_encoder = load_artifacts()
except Exception as e:
    st.error(f"Failed to load model or encoders: {e}")
    st.stop()

# ─── Streamlit UI ───────────────────────────────────────────────────────────────
st.title("💸 Health Insurance Charges Predictor")

st.markdown("""
Use the sliders and dropdowns below to enter client information,
then click **Predict** to estimate their monthly insurance charge.
""")

# Input widgets
age       = st.slider("Age", min_value=18, max_value=100, value=30)
sex       = st.radio("Sex", options=sex_encoder.classes_.tolist())
bmi       = st.number_input("BMI", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
smoker    = st.radio("Smoker", options=smoker_encoder.classes_.tolist())
region    = st.selectbox("Region", options=region_encoder.classes_.tolist())
children  = st.slider("Number of Children", min_value=0, max_value=10, value=0)

if st.button("Predict Insurance Charge"):
    # Encode and scale
    try:
        sex_enc     = sex_encoder.transform([sex])[0]
        smoker_enc  = smoker_encoder.transform([smoker])[0]
        region_enc  = region_encoder.transform([region])[0]

        X = np.array([[age, sex_enc, bmi, smoker_enc, children, region_enc]])
        X_scaled = scaler.transform(X)

        # Predict
        pred = model.predict(X_scaled)[0]
        st.success(f"💰 Estimated Insurance Charge: **${pred:,.2f}**")
    except Exception as err:
        st.error(f"Prediction error: {err}")
