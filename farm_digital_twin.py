import streamlit as st

st.set_page_config(
    page_title="Farm Digital Twin",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI Farm Digital Twin")
st.subheader("Virtual Farm Simulation System")

st.write("Simulate farm conditions and observe irrigation decisions.")

st.divider()

st.header("🌾 Virtual Farm Conditions")

soil = st.slider("Soil Moisture (%)", 0, 100, 25)
temperature = st.slider("Temperature (°C)", 0, 50, 35)
rain = st.slider("Rain Probability (%)", 0, 100, 10)
battery = st.slider("Battery Level (%)", 0, 100, 80)
solar = st.slider("Solar Energy (%)", 0, 100, 70)

st.divider()

st.header("🧠 Farm AI Simulation")

if st.button("Run Farm Simulation"):

    if battery < 25:
        status = "LOW BATTERY"
        pump = "OFF"
        reason = "Battery level is too low."

    elif rain >= 60:
        status = "RAIN SAFETY"
        pump = "OFF"
        reason = "Rain probability is high."

    elif solar < 20:
        status = "LOW SOLAR ENERGY"
        pump = "OFF"
        reason = "Solar energy is insufficient."

    elif soil < 35:
        status = "IRRIGATION RECOMMENDED"
        pump = "ON (simulation only)"
        reason = "Soil moisture is low."

    else:
        status = "IRRIGATION NOT REQUIRED"
        pump = "OFF"
        reason = "Soil moisture is sufficient."

    st.subheader("Simulation Results")
    st.metric("Soil Moisture", f"{soil}%")
    st.metric("Battery", f"{battery}%")
    st.metric("Solar Energy", f"{solar}%")

    st.success(f"Farm Status: {status}")
    st.info(f"Pump Status: {pump}")
    st.write("AI Explanation:", reason)

    st.caption("Software simulation only. No physical pump is connected.")