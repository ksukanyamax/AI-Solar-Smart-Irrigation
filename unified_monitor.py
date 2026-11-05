
import streamlit as st

st.set_page_config(
    page_title="Unified System Monitor",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI Solar Smart Irrigation")
st.subheader("Version 23 - Unified System Monitoring Dashboard")

st.caption("Central monitoring of all simulated system conditions.")

st.divider()

st.header("1. Environmental Monitoring")

col1, col2, col3 = st.columns(3)

with col1:
    soil = st.slider("Soil Moisture (%)", 0, 100, 25)

with col2:
    temperature = st.slider("Temperature (°C)", 0, 50, 30)

with col3:
    rain = st.slider("Rain Probability (%)", 0, 100, 10)

st.divider()

st.header("2. Solar and Battery Monitoring")

col1, col2 = st.columns(2)

with col1:
    solar = st.slider("Solar Energy (%)", 0, 100, 70)

with col2:
    battery = st.slider("Battery Level (%)", 0, 100, 80)

st.divider()

st.header("3. Water and Sensor Monitoring")

col1, col2 = st.columns(2)

with col1:
    water = st.number_input(
        "Available Water (Litres)",
        min_value=0,
        value=1000
    )

with col2:
    sensor = st.selectbox(
        "Sensor Condition",
        ["Healthy", "Fault Detected", "Uncertain Reading"]
    )

flow_difference = st.slider(
    "Water Flow Difference (%)",
    0, 100, 0
)

st.divider()

st.header("4. Central Decision Intelligence")

if st.button("RUN UNIFIED SYSTEM ANALYSIS"):

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

    elif flow_difference > 30:
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

    st.divider()

    st.header("5. Unified Monitoring Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Soil Moisture", f"{soil}%")
    col2.metric("Solar Energy", f"{solar}%")
    col3.metric("Battery Level", f"{battery}%")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rain Probability", f"{rain}%")
    col2.metric("Available Water", f"{water} L")
    col3.metric("Temperature", f"{temperature} °C")

    st.subheader("Central System Decision")
    st.info(decision)

    st.subheader("Pump Status")
    st.write(pump)

    st.subheader("System Explanation")
    st.write(reason)

    if decision in [
        "SAFE MODE",
        "LOW BATTERY",
        "RAIN SAFETY",
        "LOW SOLAR ENERGY",
        "POSSIBLE WATER LEAKAGE",
        "WATER UNAVAILABLE"
    ]:
        st.error("ATTENTION REQUIRED")
    else:
        st.success("SYSTEM CHECK COMPLETED")

st.divider()

st.caption(
    "Version 23 - Software simulation only. "
    "No physical sensors or pump are connected."
)
