import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Water Monitoring",
    page_icon="💧",
    layout="wide"
)

st.title("💧 Smart Water Usage & Leakage Detection")
st.subheader("Water Monitoring and Analytics Dashboard")

st.divider()

st.header("Water System Inputs")

flow_rate = st.slider("Water Flow Rate (L/min)", 0, 100, 20)
operating_time = st.slider("Pump Operating Time (Minutes)", 0, 120, 30)
expected_flow = st.slider("Expected Flow Rate (L/min)", 1, 100, 20)
actual_flow = st.slider("Actual Flow Rate (L/min)", 0, 100, 20)

st.divider()

if "water_history" not in st.session_state:
    st.session_state.water_history = []

st.header("Water System Analysis")

if st.button("Analyze Water System"):

    total_water = flow_rate * operating_time

    flow_difference = abs(actual_flow - expected_flow)

    if flow_difference > expected_flow * 0.30:
        status = "POSSIBLE WATER LEAKAGE"
        pump_status = "OFF (simulation only)"
        explanation = "Abnormal flow difference detected."
    else:
        status = "NORMAL WATER FLOW"
        pump_status = "NORMAL (simulation only)"
        explanation = "Water flow is within the expected range."

    record = {
        "Water Used (Litres)": total_water,
        "Expected Flow": expected_flow,
        "Actual Flow": actual_flow,
        "Status": status
    }

    st.session_state.water_history.append(record)

    st.subheader("Analysis Results")
    st.metric("Estimated Water Used", f"{total_water} Litres")
    st.metric("Actual Flow Rate", f"{actual_flow} L/min")

    if status == "POSSIBLE WATER LEAKAGE":
        st.error(status)
    else:
        st.success(status)

    st.info(f"Pump Status: {pump_status}")
    st.write("System Explanation:", explanation)

st.divider()

st.header("📊 Water Usage Analytics")

if st.session_state.water_history:

    history_df = pd.DataFrame(st.session_state.water_history)

    total_consumption = history_df["Water Used (Litres)"].sum()
    average_consumption = history_df["Water Used (Litres)"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Water Used", f"{total_consumption} L")
    col2.metric("Average Usage", f"{average_consumption:.1f} L")
    col3.metric("Total Tests", len(history_df))

    st.subheader("Water Consumption Chart")

    st.bar_chart(
        history_df["Water Used (Litres)"]
    )

    st.subheader("Water Usage History")
    st.dataframe(history_df, width="stretch")

else:
    st.info("Run water analysis to generate analytics.")

st.caption(
    "Software simulation only. "
    "Water readings are manually entered, not measured by physical sensors."
)