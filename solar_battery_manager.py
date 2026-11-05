import streamlit as st

st.set_page_config(
    page_title="Solar Battery Manager",
    page_icon="🔋",
    layout="wide"
)

st.title("☀️ Solar & Backup Battery Manager")
st.subheader("Smart Power Management System")

st.write("Monitor solar power and backup battery conditions.")

st.divider()

st.header("🔋 Power System Inputs")

solar = st.slider("Solar Energy Level (%)", 0, 100, 70)
battery = st.slider("Backup Battery Level (%)", 0, 100, 80)
pump_load = st.slider("Pump Power Load (Watts)", 10, 500, 100)
hours_needed = st.slider("Required Pump Operating Time (Hours)", 1, 12, 2)

st.divider()

st.header("🧠 AI Power Management")

if st.button("Analyze Power System"):

    if solar >= 30:
        power_source = "SOLAR POWER"
        explanation = "Solar energy is available."
    elif battery >= 25:
        power_source = "BACKUP BATTERY"
        explanation = "Solar energy is low. Backup battery is selected."
    else:
        power_source = "POWER SAVING MODE"
        explanation = "Solar and battery power are insufficient."

    if battery < 25:
        battery_status = "LOW BATTERY ALERT"
    elif battery < 80:
        battery_status = "BATTERY CHARGING OR AVAILABLE"
    else:
        battery_status = "BATTERY LEVEL HEALTHY"

    if battery >= 25:
        backup_hours = (battery / 100) * 5
    else:
        backup_hours = 0

    required_energy = pump_load * hours_needed

    st.subheader("Power System Results")

    st.success(f"Selected Power Source: {power_source}")
    st.info(f"Battery Status: {battery_status}")

    st.metric("Battery Level", f"{battery}%")
    st.metric("Solar Energy", f"{solar}%")
    st.metric("Estimated Backup Duration", f"{backup_hours:.1f} hours")

    st.write("AI Explanation:", explanation)

    st.write(f"Required Pump Energy: {required_energy} Wh")

    st.caption(
        "Software simulation only. Battery duration is illustrative, "
        "not a real hardware measurement."
    )