
import streamlit as st
import os

st.set_page_config(
    page_title="AI Smart Irrigation System",
    page_icon="🌱",
    layout="wide"
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))


def home():

    st.title("AI-Powered Solar Smart Irrigation")
    st.subheader("Self-Reliant Decision Intelligence Dashboard")

    st.write(
        "Central control panel for all irrigation software modules."
    )

    st.divider()

    st.header("Project Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Project Version", "27")
    col2.metric("Software Modules", "10")
    col3.metric("System Mode", "Simulation")

    st.divider()

    st.header("Available Modules")

    modules = [
        ("Advanced Irrigation Dashboard", "advanced_dashboard.py"),
        ("Farm Digital Twin", "farm_digital_twin.py"),
        ("Solar Battery Manager", "solar_battery_manager.py"),
        ("Energy Optimizer", "energy_optimizer.py"),
        ("Water Leakage Detection", "water_leakage_detection.py"),
        ("Water Saving Optimizer", "water_saving_optimizer.py"),
        ("Weather Irrigation Prediction", "weather_irrigation.py"),
        ("Smart System Integration", "system_integration.py"),
        ("Central Decision History", "decision_histrory.py"),
        ("AI Prediction Dashboard", "ai_prediction_dashboard.py")
    ]

    for name, filename in modules:

        st.subheader(name)

        file_path = os.path.join(APP_DIR, filename)

        if os.path.exists(file_path):

            st.page_link(
                filename,
                label="Open " + name,
                icon="➡️"
            )

        else:

            st.warning(
                "Module file not found: " + filename
            )

        st.divider()

    st.caption(
        "Software simulation only. "
        "No physical sensors or pump are connected."
    )


pages = [
    st.Page(home, title="Main Dashboard", icon="🌱", default=True),
    st.Page("advanced_dashboard.py", title="Advanced Irrigation"),
    st.Page("farm_digital_twin.py", title="Farm Digital Twin"),
    st.Page("solar_battery_manager.py", title="Solar Battery Manager"),
    st.Page("energy_optimizer.py", title="Energy Optimizer"),
    st.Page("water_leakage_detection.py", title="Water Leakage Detection"),
    st.Page("water_saving_optimizer.py", title="Water Saving Optimizer"),
    st.Page("weather_irrigation.py", title="Weather Prediction"),
    st.Page("system_integration.py", title="System Integration"),
    st.Page("decision_histrory.py", title="Decision History"),
    st.Page("ai_prediction_dashboard.py", title="AI Prediction Dashboard")
]

navigation = st.navigation(pages)
navigation.run()
