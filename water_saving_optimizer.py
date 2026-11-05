import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Smart Water Saving Analytics",
    page_icon="💧",
    layout="wide"
)

st.title("🌱 Smart Water Saving & Irrigation Optimizer")
st.subheader("Water Conservation and Analytics Dashboard")

st.divider()

st.header("💧 Farm Water Inputs")

farm_area = st.number_input(
    "Farm Area (Square Metres)",
    min_value=1,
    max_value=100000,
    value=100
)

soil_moisture = st.slider(
    "Soil Moisture (%)", 0, 100, 25
)

daily_water_limit = st.number_input(
    "Daily Water Limit (Litres)",
    min_value=100,
    max_value=1000000,
    value=1000
)

water_used = st.number_input(
    "Water Already Used Today (Litres)",
    min_value=0,
    max_value=1000000,
    value=400
)

water_needed_per_sqm = st.number_input(
    "Estimated Water Requirement (L/m²)",
    min_value=0.0,
    max_value=100.0,
    value=5.0
)

st.divider()

if "water_saving_history" not in st.session_state:
    st.session_state.water_saving_history = []

if st.button("Optimize Water Usage"):

    required_water = farm_area * water_needed_per_sqm

    remaining_water = max(
        0, daily_water_limit - water_used
    )

    if soil_moisture >= 60:
        decision = "IRRIGATION NOT REQUIRED"
        recommended_water = 0
        explanation = "Soil moisture is already sufficient."

    elif remaining_water == 0:
        decision = "DAILY WATER LIMIT REACHED"
        recommended_water = 0
        explanation = "Daily water allowance has been used."

    else:
        recommended_water = min(
            required_water, remaining_water
        )

        decision = "WATER-SAVING IRRIGATION"
        explanation = (
            "Water allocation is limited by estimated need "
            "and the remaining daily allowance."
        )

    water_saved = max(
        0, required_water - recommended_water
    )

    if required_water > 0:
        saving_percentage = (
            water_saved / required_water
        ) * 100
    else:
        saving_percentage = 0

    record = {
        "Estimated Requirement (L)": required_water,
        "Recommended Water (L)": recommended_water,
        "Estimated Difference (L)": water_saved,
        "Saving Percentage (%)": saving_percentage,
        "Decision": decision
    }

    st.session_state.water_saving_history.append(record)

    st.header("⚡ Optimization Results")

    st.metric("Estimated Water Requirement", f"{required_water:.1f} L")
    st.metric("Remaining Daily Water", f"{remaining_water:.1f} L")
    st.metric("Recommended Water", f"{recommended_water:.1f} L")

    st.info(f"System Decision: {decision}")
    st.write("System Explanation:", explanation)

    if decision == "IRRIGATION NOT REQUIRED":
        st.success("No irrigation is recommended.")
    elif recommended_water < required_water:
        st.warning(
            "Available water is below the estimated requirement. "
            "Check field conditions before irrigation."
        )

st.divider()

st.header("📊 Water Saving Analytics")

if st.session_state.water_saving_history:

    history_df = pd.DataFrame(
        st.session_state.water_saving_history
    )

    total_required = history_df[
        "Estimated Requirement (L)"
    ].sum()

    total_recommended = history_df[
        "Recommended Water (L)"
    ].sum()

    total_difference = history_df[
        "Estimated Difference (L)"
    ].sum()

    total_tests = len(history_df)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Estimated Requirement", f"{total_required:.1f} L")
    col2.metric("Total Recommended Water", f"{total_recommended:.1f} L")
    col3.metric("Estimated Water Difference", f"{total_difference:.1f} L")

    st.subheader("Water Usage Chart")

    chart_df = history_df[
        [
            "Estimated Requirement (L)",
            "Recommended Water (L)"
        ]
    ]

    st.bar_chart(chart_df)

    st.subheader("Water Saving History")

    st.dataframe(history_df, width="stretch")

else:
    st.info("Run water optimization to generate analytics.")

st.caption(
    "Software simulation only. Estimated water difference "
    "is not verified real-world water savings. "
    "History is stored for the current app session only."
)