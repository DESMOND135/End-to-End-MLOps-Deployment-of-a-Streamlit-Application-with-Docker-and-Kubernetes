import streamlit as st
import joblib
import numpy as np
import os

# Define the directory where the model and encoders are saved
model_dir = r"C:\Users\Administrator\Downloads\DOCKER AND KUBERNETES"

# Load model and preprocessor
model = joblib.load(os.path.join(model_dir, "model.joblib"))
scaler = joblib.load(os.path.join(model_dir, "scaler.joblib"))
sex_encoder = joblib.load(os.path.join(model_dir, "sex_encoder.joblib"))
smoker_encoder = joblib.load(os.path.join(model_dir, "smoker_encoder.joblib"))
region_encoder = joblib.load(os.path.join(model_dir, "region_encoder.joblib"))

# Streamlit UI
st.title("💸 Cost of Insurance Prediction")

# Inputs
age = st.slider("Age", 18, 100, 30)
sex = st.radio("Sex", options=["male", "female"])
bmi = st.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0)
smoker = st.radio("Smoker", options=["yes", "no"])
region = st.selectbox("Region", options=region_encoder.classes_)
children = st.slider("Number of Children", 0, 5, 0)

if st.button("Predict Insurance Cost"):
    # Encode categorical variables
    sex_encoded = sex_encoder.transform([sex])[0]
    smoker_encoded = smoker_encoder.transform([smoker])[0]
    region_encoded = region_encoder.transform([region])[0]

    # Create input array
    input_data = np.array([[age, sex_encoded, bmi, smoker_encoded, children, region_encoded]])

    # Scale the input
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)

    st.success(f"💰 Predicted Insurance Cost: ${prediction[0]:,.2f}")
