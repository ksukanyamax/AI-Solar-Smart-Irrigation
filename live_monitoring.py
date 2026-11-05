
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Live System Monitoring",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(BASE_DIR, "live_monitoring_history.json")

st.title("📊 AI Solar Smart Irrigation")
st.subheader("Version 24 - System Monitoring & History")

st.caption("Manual-input software monitoring and decision history.")

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_history(record):
    history = load_history()
    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

st.divider()

st.header("1. Monitoring Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    soil = st.slider("Soil Moisture (%)", 0, 100, 25)

with col2:
    battery = st.slider("Battery Level (%)", 0, 100, 80)

with col3:
    solar = st.slider("Solar Energy (%)", 0, 100, 70)

col1, col2 = st.columns(2)

with col1:
    rain = st.slider("Rain Probability (%)", 0, 100, 10)

with col2:
    temperature = st.slider("Temperature (°C)", 0, 50, 30)

sensor = st.selectbox(
    "Sensor Condition",
    ["Healthy", "Fault Detected", "Uncertain Reading"]
)

water = st.number_input(
    "Available Water (Litres)",
    min_value=0,
    value=1000
)

flow = st.slider("Water Flow Difference (%)", 0, 100, 0)

st.divider()

st.header("2. System Analysis")

if st.button("ANALYZE AND SAVE SYSTEM DATA"):

    if sensor != "Healthy":
        decision = "SAFE MODE"
        pump = "OFF"
        reason = "Sensor problem detected."

    elif battery < 25:
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

    elif flow > 30:
        decision = "POSSIBLE WATER LEAKAGE"
        pump = "OFF"
        reason = "Abnormal water flow difference."

    elif water <= 0:
        decision = "WATER UNAVAILABLE"
        pump = "OFF"
        reason = "No water is available."

    elif soil < 35:
        decision = "IRRIGATION RECOMMENDED"
        pump = "ON (simulation only)"
        reason = "Soil moisture is low."

    else:
        decision = "IRRIGATION NOT REQUIRED"
        pump = "OFF"
        reason = "Soil moisture is sufficient."

    record = {
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture": soil,
        "battery": battery,
        "solar_energy": solar,
        "rain_probability": rain,
        "temperature": temperature,
        "sensor_condition": sensor,
        "available_water": water,
        "flow_difference": flow,
        "decision": decision,
        "pump_status": pump,
        "explanation": reason
    }

    save_history(record)

    st.success("System data saved successfully!")
    st.info("System Decision: " + decision)
    st.write("Pump Status:", pump)
    st.write("Explanation:", reason)

st.divider()

st.header("3. Monitoring History")

history = load_history()

if history:

    df = pd.DataFrame(history)

    st.metric("Total Monitoring Records", len(df))

    st.subheader("Soil Moisture History")
    st.line_chart(df["soil_moisture"])

    st.subheader("Battery History")
    st.line_chart(df["battery"])

    st.subheader("Solar Energy History")
    st.line_chart(df["solar_energy"])

    st.subheader("Complete Decision History")
    st.dataframe(df, width="stretch")

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Monitoring History (CSV)",
        data=csv_data,
        file_name="live_monitoring_history.csv",
        mime="text/csv"
    )

else:
    st.info("No monitoring records available. Run system analysis first.")

st.caption(
    "Version 24 - Software simulation only. "
    "Inputs are manual; no live sensors or physical pump are connected."
)
