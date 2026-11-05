import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="Central Decision History",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Central System Decision History")
st.subheader("Version 22 - Permanent Decision Records")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(BASE_DIR, "central_decision_history.json")


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

st.header("Enter System Conditions")

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
    sensor = st.selectbox(
        "Sensor Condition",
        ["Healthy", "Fault Detected", "Uncertain Reading"]
    )

water_difference = st.slider(
    "Water Flow Difference (%)", 0, 100, 0
)

water_available = st.number_input(
    "Available Water (Litres)",
    min_value=0,
    value=1000
)

st.divider()

if st.button("SAVE CENTRAL SYSTEM DECISION"):

    if sensor != "Healthy":
        decision = "SAFE MODE"
        pump = "OFF"

    elif battery < 25:
        decision = "LOW BATTERY"
        pump = "OFF"

    elif rain >= 60:
        decision = "RAIN SAFETY"
        pump = "OFF"

    elif solar < 20:
        decision = "LOW SOLAR ENERGY"
        pump = "OFF"

    elif water_difference > 30:
        decision = "POSSIBLE WATER LEAKAGE"
        pump = "OFF"

    elif water_available <= 0:
        decision = "WATER UNAVAILABLE"
        pump = "OFF"

    elif soil < 35:
        decision = "IRRIGATION RECOMMENDED"
        pump = "ON (simulation only)"

    else:
        decision = "IRRIGATION NOT REQUIRED"
        pump = "OFF"

    record = {
        "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture": soil,
        "battery": battery,
        "solar_energy": solar,
        "rain_probability": rain,
        "sensor_condition": sensor,
        "water_flow_difference": water_difference,
        "available_water": water_available,
        "decision": decision,
        "pump_status": pump
    }

    save_history(record)

    st.success("Decision saved successfully!")
    st.info("System Decision: " + decision)
    st.write("Pump Status:", pump)

st.divider()

st.header("📚 Saved Decision History")

history = load_history()

if history:

    st.metric("Total Saved Decisions", len(history))

    st.dataframe(
        history,
        width="stretch"
    )

    history_json = json.dumps(history, indent=4)

    st.download_button(
        label="Download Decision History (JSON)",
        data=history_json,
        file_name="central_decision_history.json",
        mime="application/json"
    )

else:
    st.info("No saved decisions yet. Run an analysis first.")

st.caption(
    "Version 22 - Software simulation only. "
    "No physical sensors or pump are connected."
)