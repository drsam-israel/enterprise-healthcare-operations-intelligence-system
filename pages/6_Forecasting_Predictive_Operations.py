import streamlit as st
import plotly.express as px
import pandas as pd

from utils.data_loader import load_hospital_data
from utils.filters import apply_global_filters

st.set_page_config(
    page_title="Forecasting & Predictive Operations",
    layout="wide"
)

df = load_hospital_data()
df = apply_global_filters(df)

# ---------------------------------------------------
# SIDEBAR BRANDING
# ---------------------------------------------------

st.sidebar.title("Hospital Operations")
st.sidebar.subheader("Command Center")

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    **System:** Enterprise Healthcare Operations Intelligence System  
    **Focus:** Workflow, Capacity & Executive Operations Analytics
    """
)

st.sidebar.markdown("---")
st.sidebar.success("Operational System Online")

st.title("Forecasting & Predictive Operations")
st.subheader("Operational Forecasting, Capacity Planning & Executive Predictive Intelligence")

st.markdown("---")

st.header("Forecasting Overview")

col1, col2, col3 = st.columns(3)

with col1:
    if "length_of_stay_days" in df.columns:
        avg_los = round(df["length_of_stay_days"].mean(), 2)
        st.metric("Average LOS Baseline", f"{avg_los} days")

with col2:
    if "capacity_pressure_score" in df.columns:
        avg_pressure = round(df["capacity_pressure_score"].mean(), 2)
        st.metric("Average Capacity Pressure", avg_pressure)

with col3:
    if "ed_wait_time_minutes" in df.columns:
        avg_ed_wait = round(df["ed_wait_time_minutes"].mean(), 2)
        st.metric("Average ED Wait Time", f"{avg_ed_wait} mins")

st.markdown("---")

st.header("Operational Forecasting Intelligence")

forecast_col1, forecast_col2 = st.columns(2)

with forecast_col1:
    if "hospital_unit" in df.columns:
        admissions_forecast = (
            df["hospital_unit"]
            .value_counts()
            .reset_index()
        )

        admissions_forecast.columns = ["hospital_unit", "projected_volume"]

        admissions_forecast["forecasted_next_period"] = (
            admissions_forecast["projected_volume"] * 1.08
        ).round(0)

        fig_forecast = px.bar(
            admissions_forecast,
            x="hospital_unit",
            y="forecasted_next_period",
            title="Projected Operational Volume by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "forecasted_next_period": "Projected Volume"
            }
        )

        st.plotly_chart(
            fig_forecast,
            use_container_width=True,
            key="forecast_volume_chart"
        )

with forecast_col2:
    if "hospital_unit" in df.columns and "capacity_pressure_score" in df.columns:
        pressure_projection = (
            df.groupby("hospital_unit")["capacity_pressure_score"]
            .mean()
            .reset_index()
        )

        pressure_projection["projected_pressure"] = (
            pressure_projection["capacity_pressure_score"] * 1.05
        ).round(2)

        fig_pressure = px.line(
            pressure_projection,
            x="hospital_unit",
            y="projected_pressure",
            markers=True,
            title="Projected Capacity Pressure by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "projected_pressure": "Projected Capacity Pressure"
            }
        )

        st.plotly_chart(
            fig_pressure,
            use_container_width=True,
            key="forecast_pressure_chart"
        )

st.markdown("---")

st.header("Executive Forecasting Signals")

signal_col1, signal_col2, signal_col3 = st.columns(3)

with signal_col1:
    if avg_pressure >= 80:
        st.error("Projected Critical Capacity Pressure")
    elif avg_pressure >= 60:
        st.warning("Projected Moderate Capacity Pressure")
    else:
        st.success("Projected Capacity Stable")

with signal_col2:
    if avg_ed_wait >= 90:
        st.error("Projected Severe ED Congestion")
    elif avg_ed_wait >= 60:
        st.warning("Projected Moderate ED Congestion")
    else:
        st.success("Projected ED Flow Stable")

with signal_col3:
    st.info(
        "Forecasting intelligence supports proactive operational planning, "
        "resource allocation, and executive preparedness."
    )

st.markdown("---")

st.header("Operational Interpretation")

st.write(
    """
    This page provides lightweight operational forecasting and predictive
    healthcare operations intelligence. It supports executive teams in
    anticipating workflow pressure, projected hospital utilization,
    operational congestion, and future capacity strain. Forecasting is used
    strategically to support healthcare operational preparedness and
    executive decision-making.
    """
)