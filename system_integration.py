import streamlit as st

st.set_page_config(
    page_title="Smart System Integration",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI Smart Irrigation - Central System Monitor")
st.subheader("Version 21 | Smart System Integration")

st.caption("Central monitoring of all irrigation system modules.")

st.divider()

st.header("1. Soil & Weather Status")

col1, col2, col3 = st.columns(3)

with col1:
    soil = st.slider("Soil Moisture (%)", 0, 100, 25)

with col2:
    temperature = st.slider("Temperature (°C)", 0, 50, 30)

with col3:
    rain = st.slider("Rain Probability (%)", 0, 100, 10)

st.divider()

st.header("2. Solar & Battery Status")

col1, col2 = st.columns(2)

with col1:
    solar = st.slider("Solar Energy (%)", 0, 100, 70)

with col2:
    battery = st.slider("Battery Level (%)", 0, 100, 80)

st.divider()

st.header("3. Water System Status")

col1, col2 = st.columns(2)

with col1:
    water_available = st.number_input(
        "Available Water (Litres)",
        min_value=0,
        value=1000
    )

with col2:
    flow_difference = st.slider(
        "Water Flow Difference (%)",
        0, 100, 0
    )

st.divider()

st.header("4. Sensor Health")

sensor_health = st.selectbox(
    "Sensor Condition",
    ["Healthy", "Fault Detected", "Uncertain Reading"]
)

st.divider()

if st.button("RUN CENTRAL SYSTEM ANALYSIS"):

    alerts = []

    if sensor_health != "Healthy":
        decision = "SAFE MODE"
        pump = "OFF"
        alerts.append("Sensor problem detected.")

    elif battery < 25:
        decision = "LOW BATTERY"
        pump = "OFF"
        alerts.append("Battery level is too low.")

    elif rain >= 60:
        decision = "RAIN SAFETY"
        pump = "OFF"
        alerts.append("Rain probability is high.")

    elif solar < 20:
        decision = "LOW SOLAR ENERGY"
        pump = "OFF"
        alerts.append("Solar energy is insufficient.")

    elif flow_difference > 30:
        decision = "POSSIBLE WATER LEAKAGE"
        pump = "OFF"
        alerts.append("Abnormal water flow difference.")

    elif water_available <= 0:
        decision = "WATER UNAVAILABLE"
        pump = "OFF"
        alerts.append("No available water.")

    elif soil < 35:
        decision = "IRRIGATION RECOMMENDED"
        pump = "ON (simulation only)"

    else:
        decision = "IRRIGATION NOT REQUIRED"
        pump = "OFF"

    st.divider()

    st.header("5. Central System Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Soil Moisture", f"{soil}%")
    col2.metric("Battery Level", f"{battery}%")
    col3.metric("Solar Energy", f"{solar}%")

    st.subheader("System Decision")
    st.info(decision)

    st.subheader("Pump Status")
    st.write(pump)

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("All basic safety checks passed.")

    st.subheader("AI System Explanation")

    st.write(
        f"Decision: {decision}. "
        f"Soil moisture: {soil}%. "
        f"Rain probability: {rain}%. "
        f"Battery: {battery}%. "
        f"Solar energy: {solar}%."
    )

    st.subheader("Overall System Health")

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
    "Version 21 is a manual-input software simulation. "
    "It does not yet read live sensors or control a physical pump."
)