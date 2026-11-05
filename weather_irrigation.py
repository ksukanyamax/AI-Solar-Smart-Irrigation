import streamlit as st

st.set_page_config(
    page_title="Weather-Based Smart Irrigation",
    page_icon="🌦️",
    layout="wide"
)

st.title("Weather-Based Smart Irrigation")
st.subheader("Weather-Aware Water Management System")

st.write(
    "Analyze soil and weather conditions "
    "before making an irrigation decision."
)

st.divider()

st.header("Farm and Weather Inputs")

soil = st.slider(
    "Soil Moisture (%)",
    min_value=0,
    max_value=100,
    value=25
)

temperature = st.slider(
    "Temperature (Celsius)",
    min_value=0,
    max_value=50,
    value=30
)

rain = st.slider(
    "Rain Probability (%)",
    min_value=0,
    max_value=100,
    value=20
)

battery = st.slider(
    "Battery Level (%)",
    min_value=0,
    max_value=100,
    value=80
)

st.divider()

if st.button("Predict Irrigation"):

    if battery < 25:
        decision = "LOW BATTERY"
        pump = "OFF"
        reason = "Battery is below the safety limit."

    elif rain >= 60:
        decision = "RAIN SAFETY"
        pump = "OFF"
        reason = "Rain probability is high."

    elif soil >= 60:
        decision = "IRRIGATION NOT REQUIRED"
        pump = "OFF"
        reason = "Soil moisture is sufficient."

    elif temperature >= 40 and soil < 35:
        decision = "HIGH WATER NEED"
        pump = "ON (simulation only)"
        reason = (
            "High temperature and low soil moisture "
            "indicate possible water need."
        )

    elif soil < 35:
        decision = "IRRIGATION RECOMMENDED"
        pump = "ON (simulation only)"
        reason = (
            "Soil moisture is low and rain probability "
            "is not high."
        )

    else:
        decision = "MONITOR SOIL"
        pump = "OFF"
        reason = "Continue monitoring soil moisture."

    st.divider()

    st.header("Prediction Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Soil Moisture", f"{soil}%")
    col2.metric("Temperature", f"{temperature} C")
    col3.metric("Rain Probability", f"{rain}%")

    st.info(f"System Decision: {decision}")
    st.write(f"Pump Status: {pump}")
    st.write(f"System Explanation: {reason}")

    if pump == "OFF":
        st.warning("Irrigation is currently stopped in this simulation.")
    else:
        st.success("Irrigation is recommended in this simulation.")

st.divider()

st.caption(
    "Software simulation only. Weather values are entered manually. "
    "This is not a live weather forecast and no physical pump is connected."
)