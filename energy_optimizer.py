import streamlit as st

st.set_page_config(
    page_title="AI Energy Optimizer",
    page_icon="🔋",
    layout="wide"
)

st.title("☀️ AI Solar Energy Optimizer")
st.subheader("Intelligent Battery Charging & Energy Management")

st.divider()

st.header("🔋 Energy System Inputs")

solar_energy = st.slider("Available Solar Energy (%)", 0, 100, 70)
battery_level = st.slider("Current Battery Level (%)", 0, 100, 40)
pump_power = st.slider("Pump Power (Watts)", 10, 500, 100)
operating_hours = st.slider("Pump Operating Hours", 1, 12, 2)

st.divider()

if st.button("Optimize Energy"):

    charging_energy = max(0, solar_energy - 20) * 0.2

    new_battery = min(100, battery_level + charging_energy)

    required_energy = pump_power * operating_hours

    if solar_energy >= 30:
        power_source = "SOLAR POWER"
    elif battery_level >= 25:
        power_source = "BACKUP BATTERY"
    else:
        power_source = "POWER SAVING MODE"

    if battery_level < 25 and solar_energy < 30:
        decision = "PUMP OFF - LOW ENERGY"
        explanation = "Solar and battery energy are insufficient."
    elif new_battery < 25 and solar_energy < 30:
        decision = "PUMP OFF - BATTERY PROTECTION"
        explanation = "Battery protection is activated."
    else:
        decision = "ENERGY MANAGEMENT ACTIVE"
        explanation = "Available energy is being managed."

    st.header("⚡ Optimization Results")

    st.metric("Current Battery", f"{battery_level}%")
    st.metric("Estimated Battery After Charging", f"{new_battery:.1f}%")
    st.metric("Solar Charging Gain", f"{charging_energy:.1f}%")
    st.metric("Required Pump Energy", f"{required_energy} Wh")

    st.success(f"Selected Power Source: {power_source}")
    st.info(f"System Decision: {decision}")

    st.write("AI Explanation:", explanation)

    st.caption(
        "Illustrative software simulation only. "
        "Real battery charging requires hardware measurements."
    )