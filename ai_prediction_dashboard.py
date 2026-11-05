
import streamlit as st
import pandas as pd
import joblib
import os

# VERSION 26 - AI PREDICTION DASHBOARD

st.set_page_config(
    page_title="AI Prediction Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Powered Solar Smart Irrigation")
st.subheader("Version 26 - AI Prediction Dashboard")

st.caption(
    "AI prediction with integrated safety decision system."
)

# Load trained AI model
MODEL_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "models",
    "irrigation_prediction_model.pkl"
)

if not os.path.exists(MODEL_FILE):
    st.error("Trained AI model not found!")
    st.stop()

try:
    model = joblib.load(MODEL_FILE)
    st.success("AI Model Loaded Successfully!")
except Exception as error:
    st.error(f"Model loading failed: {error}")
    st.stop()

st.divider()

# 1. Farm Conditions
st.header("1. Farm Conditions")

col1, col2, col3 = st.columns(3)

with col1:
    soil = st.slider(
        "Soil Moisture (%)",
        0, 100, 25
    )

with col2:
    temperature = st.slider(
        "Temperature (°C)",
        0, 50, 35
    )

with col3:
    rain = st.slider(
        "Rain Probability (%)",
        0, 100, 10
    )

col1, col2 = st.columns(2)

with col1:
    battery = st.slider(
        "Battery Level (%)",
        0, 100, 80
    )

with col2:
    solar = st.slider(
        "Solar Energy (%)",
        0, 100, 70
    )

st.divider()

# 2. AI Analysis
st.header("2. AI Prediction and Safety Analysis")

if st.button("RUN AI SYSTEM ANALYSIS"):

    input_data = pd.DataFrame({
        "soil_moisture": [soil],
        "temperature": [temperature],
        "rain_probability": [rain]
    })

    # AI prediction
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        ai_result = "IRRIGATION NEEDED"
    else:
        ai_result = "IRRIGATION NOT NEEDED"

    # Safety decision layer
    if battery < 25:

        decision = "LOW BATTERY"
        pump = "OFF"
        reason = "Battery is below the safety limit."

    elif rain >= 60:

        decision = "RAIN SAFETY"
        pump = "OFF"
        reason = "Rain probability is high."

    elif solar < 20:

        decision = "LOW SOLAR ENERGY"
        pump = "OFF"
        reason = "Solar energy is insufficient."

    elif prediction == 1:

        decision = "IRRIGATION RECOMMENDED"
        pump = "ON (simulation only)"
        reason = "AI predicts irrigation is needed."

    else:

        decision = "IRRIGATION NOT REQUIRED"
        pump = "OFF"
        reason = "AI predicts irrigation is not needed."

    st.divider()

    # 3. Results
    st.header("3. AI Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Soil Moisture", f"{soil}%")
    col2.metric("Battery Level", f"{battery}%")
    col3.metric("Solar Energy", f"{solar}%")

    st.subheader("AI Prediction")
    st.info(ai_result)

    st.subheader("Final System Decision")

    if pump.startswith("ON"):
        st.success(decision)
    else:
        st.warning(decision)

    st.subheader("Pump Status")

    if pump.startswith("ON"):
        st.success(pump)
    else:
        st.error(pump)

    st.subheader("AI System Explanation")
    st.write(reason)

    st.divider()

    st.subheader("System Safety Status")

    if decision in [
        "LOW BATTERY",
        "RAIN SAFETY",
        "LOW SOLAR ENERGY"
    ]:
        st.error("SAFETY CONDITION DETECTED")
    else:
        st.success("BASIC SAFETY CHECKS PASSED")

st.divider()

st.header("4. Project Information")

st.write("Project: AI-Powered Solar Smart Irrigation")
st.write("Version: 26")
st.write("AI Model: Random Forest Classifier")
st.write("Decision System: AI + Safety Rules")
st.write("Operating Mode: Software Simulation")

st.caption(
    "Important: Model uses a small synthetic dataset. "
    "Results are not validated for real farms. "
    "No physical sensors or pump are connected."
)
