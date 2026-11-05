
import os
import json
import math
import pandas as pd
import streamlit as st

from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline


# ==========================================
# VERSION 11 - AI SOLAR SMART IRRIGATION
# ==========================================

st.set_page_config(
    page_title="AI Solar Smart Irrigation",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI-Powered Solar Smart Irrigation")
st.subheader("Advanced Dashboard - Version 11")


# ==========================================
# FILE PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

HISTORY_FILE = os.path.join(
    BASE_DIR,
    "irrigation_history.json"
)


# ==========================================
# SYNTHETIC AI TRAINING DATA
# ==========================================

data = {
    "soil": [
        10, 15, 20, 25, 30, 35,
        40, 45, 50, 55, 60, 65,
        70, 75, 80, 85, 90, 95,
        18, 22, 28, 38, 48, 58
    ],

    "temperature": [
        35, 38, 36, 34, 32, 30,
        28, 27, 26, 25, 24, 23,
        22, 21, 20, 19, 18, 17,
        37, 35, 33, 29, 26, 24
    ],

    "rain": [
        5, 10, 15, 10, 20, 25,
        30, 35, 40, 45, 50, 55,
        60, 65, 70, 75, 80, 85,
        10, 15, 20, 30, 45, 60
    ],

    "pump": [
        1, 1, 1, 1, 1, 1,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        1, 1, 1, 0, 0, 0
    ]
}

df = pd.DataFrame(data)

X = df[["soil", "temperature", "rain"]]
y = df["pump"]


# ==========================================
# AI MODEL
# ==========================================

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        max_depth=4,
        random_state=42
    ))
])

model.fit(X, y)


# ==========================================
# HISTORY FUNCTIONS
# ==========================================

def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

        if isinstance(history, list):
            return history

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_history(record):

    history = load_history()
    history.append(record)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


# ==========================================
# FARM SENSOR INPUTS
# ==========================================

st.divider()
st.header("🌾 Farm Sensor Information")

col1, col2, col3 = st.columns(3)

with col1:
    soil = st.number_input(
        "Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0
    )

with col2:
    temperature = st.number_input(
        "Temperature (°C)",
        min_value=-10.0,
        max_value=60.0,
        value=35.0
    )

with col3:
    rain = st.number_input(
        "Rain Probability (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0
    )

col4, col5 = st.columns(2)

with col4:
    battery = st.number_input(
        "Battery Level (%)",
        min_value=0.0,
        max_value=100.0,
        value=80.0
    )

with col5:
    solar = st.number_input(
        "Solar Energy (%)",
        min_value=0.0,
        max_value=100.0,
        value=70.0
    )


# ==========================================
# RECENT SOIL READINGS
# ==========================================

st.divider()
st.header("📡 Recent Soil Sensor Readings")

r1, r2, r3, r4, r5 = st.columns(5)

with r1:
    recent1 = st.number_input("Reading 1", value=18.0)

with r2:
    recent2 = st.number_input("Reading 2", value=19.0)

with r3:
    recent3 = st.number_input("Reading 3", value=20.0)

with r4:
    recent4 = st.number_input("Reading 4", value=21.0)

with r5:
    recent5 = st.number_input("Reading 5", value=20.0)


# ==========================================
# FARM CONDITION ANALYSIS
# ==========================================

st.divider()

if st.button("🔍 Analyze Farm Conditions", type="primary"):

    readings = [
        soil, temperature, rain, battery, solar,
        recent1, recent2, recent3, recent4, recent5
    ]

    faults = []

    if not all(math.isfinite(v) for v in readings):
        faults.append("Invalid numerical sensor data.")

    recent = [
        recent1, recent2, recent3, recent4, recent5
    ]

    if not all(
        math.isfinite(v) and 0 <= v <= 100
        for v in recent
    ):
        faults.append("Recent soil readings are invalid.")

    if not faults and len(set(recent)) == 1:
        faults.append("Suspicious stuck soil sensor.")

    status = ""
    pump = "OFF"
    explanation = ""

    if faults:

        status = "SAFE MODE"
        explanation = "; ".join(faults)

        st.error("🚨 SAFE MODE")
        st.write("Pump: OFF")
        st.write("Fault:", explanation)

    elif battery < 25:

        status = "LOW BATTERY"
        explanation = "Battery level is too low."

        st.warning("🔋 LOW BATTERY")
        st.write("Pump: OFF")
        st.write(explanation)

    else:

        input_data = pd.DataFrame(
            [[soil, temperature, rain]],
            columns=["soil", "temperature", "rain"]
        )

        prediction = model.predict(input_data)[0]

        if rain >= 60:

            status = "RAIN SAFETY"
            explanation = "Rain probability is high."

            st.warning("🌧️ RAIN SAFETY")
            st.write("Pump: OFF")
            st.write(explanation)

        elif solar < 20:

            status = "LOW SOLAR ENERGY"
            explanation = "Solar energy level is too low."

            st.warning("☀️ LOW SOLAR ENERGY")
            st.write("Pump: OFF")
            st.write(explanation)

        elif prediction == 1:

            status = "IRRIGATION RECOMMENDED"
            pump = "ON (simulation only)"
            explanation = "AI model recommends irrigation."

            st.success("🌱 IRRIGATION RECOMMENDED")
            st.write("Pump: ON (simulation only)")
            st.write(explanation)

        else:

            status = "IRRIGATION NOT REQUIRED"
            explanation = "AI model does not recommend irrigation."

            st.info("💧 IRRIGATION NOT REQUIRED")
            st.write("Pump: OFF")
            st.write(explanation)

    # SAVE RESULT

    record = {
        "date_time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "soil_moisture": soil,
        "temperature": temperature,
        "rain_probability": rain,
        "battery": battery,
        "solar_energy": solar,
        "status": status,
        "pump": pump
    }

    save_history(record)

    st.info("Sensor checks completed.")
    st.success("Irrigation decision saved to history.")


# ==========================================
# IRRIGATION HISTORY
# ==========================================

st.divider()
st.header("📊 Irrigation History")

history = load_history()

if history:

    history_df = pd.DataFrame(history)

    st.dataframe(
        history_df,
        width="stretch"
    )

    st.success(
        f"Total Records: {len(history)}"
    )

else:

    st.info("No irrigation history found yet.")


# ==========================================
# VERSION 11 - DATA ANALYTICS
# ==========================================

st.divider()
st.header("📈 Irrigation Data Analytics")

if history:

    analytics_df = pd.DataFrame(history)

    analytics_df["date_time"] = pd.to_datetime(
        analytics_df["date_time"],
        errors="coerce"
    )

    analytics_df = analytics_df.dropna(
        subset=["date_time"]
    ).sort_values("date_time")

    # SOIL MOISTURE GRAPH

    st.subheader("🌱 Soil Moisture History")

    st.line_chart(
        analytics_df,
        x="date_time",
        y="soil_moisture"
    )

    # BATTERY GRAPH

    st.subheader("🔋 Battery Level History")

    st.line_chart(
        analytics_df,
        x="date_time",
        y="battery"
    )

    # SOLAR ENERGY GRAPH

    st.subheader("☀️ Solar Energy History")

    st.line_chart(
        analytics_df,
        x="date_time",
        y="solar_energy"
    )

    # TEMPERATURE GRAPH

    st.subheader("🌡️ Temperature History")

    st.line_chart(
        analytics_df,
        x="date_time",
        y="temperature"
    )

    # RAIN GRAPH

    st.subheader("💧 Rain Probability History")

    st.line_chart(
        analytics_df,
        x="date_time",
        y="rain_probability"
    )

    # ANALYTICS SUMMARY

    st.divider()
    st.subheader("📋 Analytics Summary")

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Average Soil Moisture",
            f"{analytics_df['soil_moisture'].mean():.1f}%"
        )

    with metric2:
        st.metric(
            "Average Battery",
            f"{analytics_df['battery'].mean():.1f}%"
        )

    with metric3:
        st.metric(
            "Total Records",
            len(analytics_df)
        )

else:

    st.info(
        "No irrigation data available. "
        "Analyze farm conditions to create records."
    )


# ==========================================
# PROJECT INFORMATION
# ==========================================

st.divider()

st.caption(
    "AI Solar Smart Irrigation - Software Simulation Prototype"
)

st.caption(
    "Pump control is simulated. No physical pump is connected."
)

st.caption(
    "AI predictions use synthetic demonstration data "
    "and are not yet validated with real farm data."
)
# VERSION 12 - CSV EXPORT

st.divider()
st.header("📥 Download Irrigation Data")

if history:
    export_df = pd.DataFrame(history)

    csv_data = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Irrigation History (CSV)",
        data=csv_data,
        file_name="irrigation_history.csv",
        mime="text/csv"
    )

    st.success("Your irrigation history is ready to download!")

else:
    st.info("No irrigation history available to download.")
    # VERSION 13 - AI DECISION EXPLANATION

st.divider()
st.header("🧠 AI Decision Explanation")

if "status" in locals():

    if status == "IRRIGATION RECOMMENDED":
        explanation = (
            "Soil conditions indicate that irrigation is needed. "
            "Rain probability is low and available energy is sufficient."
        )

    elif status == "SAFE MODE":
        explanation = (
            "The system detected suspicious sensor readings. "
            "Irrigation is stopped to prevent unsafe operation."
        )

    elif status == "LOW BATTERY":
        explanation = (
            "Battery level is below the safety limit. "
            "The pump remains OFF to protect the battery."
        )

    elif status == "RAIN SAFETY":
        explanation = (
            "Rain probability is high. "
            "Irrigation is paused to avoid unnecessary watering."
        )

    elif status == "LOW SOLAR ENERGY":
        explanation = (
            "Available solar energy is too low. "
            "Irrigation is paused to save energy."
        )

    else:
        explanation = "No decision explanation is available."

    st.info("AI Explanation: " + explanation)

else:
    st.info("Run sensor analysis to view the AI decision explanation.")