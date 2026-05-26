import streamlit as st
import plotly.express as px

from utils.data_loader import load_hospital_data
from utils.filters import apply_global_filters

st.set_page_config(
    page_title="Capacity & Bed Intelligence",
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

st.title("Capacity & Bed Intelligence")
st.subheader("Hospital Occupancy, Bed Utilization, ICU Pressure & Capacity Monitoring")

st.markdown("---")

st.header("Capacity Overview")

col1, col2, col3 = st.columns(3)

with col1:
    if "bed_occupancy_status" in df.columns:
        occupied_beds = df[df["bed_occupancy_status"] == "Occupied"].shape[0]
        st.metric("Occupied Beds", f"{occupied_beds:,}")

with col2:
    if "bed_occupancy_status" in df.columns:
        available_beds = df[df["bed_occupancy_status"] == "Available"].shape[0]
        st.metric("Available Beds", f"{available_beds:,}")

with col3:
    if "capacity_pressure_score" in df.columns:
        avg_pressure = round(df["capacity_pressure_score"].mean(), 2)
        st.metric("Avg Capacity Pressure", avg_pressure)

st.markdown("---")

st.header("Unit-Level Capacity Intelligence")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if "hospital_unit" in df.columns and "bed_occupancy_status" in df.columns:
        occupancy_by_unit = (
            df.groupby(["hospital_unit", "bed_occupancy_status"])
            .size()
            .reset_index(name="bed_count")
        )

        fig_occ = px.bar(
            occupancy_by_unit,
            x="hospital_unit",
            y="bed_count",
            color="bed_occupancy_status",
            title="Bed Occupancy Status by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "bed_count": "Bed Count",
                "bed_occupancy_status": "Bed Status"
            }
        )

        st.plotly_chart(fig_occ, use_container_width=True, key="bed_occupancy_by_unit")

with chart_col2:
    if "hospital_unit" in df.columns and "capacity_pressure_score" in df.columns:
        pressure_by_unit = (
            df.groupby("hospital_unit")["capacity_pressure_score"]
            .mean()
            .reset_index()
            .sort_values("capacity_pressure_score", ascending=False)
        )

        fig_pressure = px.bar(
            pressure_by_unit,
            x="hospital_unit",
            y="capacity_pressure_score",
            title="Average Capacity Pressure by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "capacity_pressure_score": "Capacity Pressure Score"
            }
        )

        st.plotly_chart(fig_pressure, use_container_width=True, key="capacity_pressure_by_unit")

st.markdown("---")

st.header("ICU Capacity Monitoring")

icu_col1, icu_col2 = st.columns(2)

with icu_col1:
    if "icu_flag" in df.columns:
        icu_cases = df[df["icu_flag"] == 1].shape[0]
        non_icu_cases = df[df["icu_flag"] == 0].shape[0]

        icu_data = {
            "Care Level": ["ICU", "Non-ICU"],
            "Patient Count": [icu_cases, non_icu_cases]
        }

        fig_icu = px.pie(
            icu_data,
            names="Care Level",
            values="Patient Count",
            title="ICU vs Non-ICU Patient Distribution"
        )

        st.plotly_chart(fig_icu, use_container_width=True, key="icu_distribution_capacity")

with icu_col2:
    if "hospital_unit" in df.columns and "icu_flag" in df.columns:
        icu_by_unit = (
            df.groupby("hospital_unit")["icu_flag"]
            .sum()
            .reset_index()
            .sort_values("icu_flag", ascending=False)
        )

        fig_icu_unit = px.bar(
            icu_by_unit,
            x="hospital_unit",
            y="icu_flag",
            title="ICU Patient Load by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "icu_flag": "ICU Patient Load"
            }
        )

        st.plotly_chart(fig_icu_unit, use_container_width=True, key="icu_load_by_unit_capacity")

st.markdown("---")

st.header("Operational Interpretation")

st.write(
    """
    This page provides capacity and bed utilization intelligence across hospital units.
    It supports operational leaders in monitoring occupancy, ICU pressure, available
    bed supply, and capacity strain. These insights are critical for hospital flow
    management, resource allocation, and executive operational decision-making.
    """
)