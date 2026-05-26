import streamlit as st
import plotly.express as px

from utils.data_loader import load_hospital_data
from utils.kpi_calculations import (
    calculate_total_admissions,
    calculate_avg_los,
    calculate_icu_utilization,
    calculate_avg_ed_wait,
    calculate_total_operational_cost,
    calculate_avg_capacity_pressure
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Enterprise Healthcare Operations Intelligence System",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM EXECUTIVE STYLING
# ---------------------------------------------------

st.markdown(
    """
    <style>
    .main {
    background-color: #f8fafc;
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

    h1 {
    font-size: 42px;
    font-weight: 700;
}

h2 {
    font-size: 28px;
    margin-top: 20px;
}

h3 {
    font-size: 22px;
}
    [data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #dbe4ee;
    box-shadow: 0px 4px 14px rgba(15, 23, 42, 0.06);
}
    [data-testid="stMetricLabel"] {
        font-size: 15px;
        color: #334155;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        font-size: 30px;
        color: #0f172a;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #172554 100%
    );
}

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = load_hospital_data()


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

st.sidebar.markdown(
    """
    ### Core Modules
    - Executive Command Center
    - Patient Flow Intelligence
    - Capacity & Bed Intelligence
    - ED Congestion Intelligence
    - LOS & Utilization Analytics
    - Financial Operations Intelligence
    """
)
# ---------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------

total_admissions = calculate_total_admissions(df)
avg_los = calculate_avg_los(df)
icu_utilization = calculate_icu_utilization(df)
avg_ed_wait = calculate_avg_ed_wait(df)
total_cost = calculate_total_operational_cost(df)
capacity_pressure = calculate_avg_capacity_pressure(df)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("Enterprise Healthcare Operations Intelligence System")

st.subheader(
    "Enterprise Hospital Workflow, Capacity & Executive Operations Analytics System"
)

st.info(
    """
    Executive command-center environment for monitoring hospital workflow,
    capacity pressure, ICU utilization, emergency department congestion,
    length-of-stay performance, financial operations, and operational forecasting.
    """
)
st.markdown("---")

# ---------------------------------------------------
# EXECUTIVE KPI DASHBOARD
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Admissions", f"{total_admissions:,}")

with col2:
    st.metric("Average LOS (Days)", avg_los)

with col3:
    st.metric("ICU Utilization (%)", icu_utilization)

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Average ED Wait (Minutes)", avg_ed_wait)

with col5:
    st.metric("Operational Cost (USD)", f"${total_cost:,.0f}")

with col6:
    st.metric("Capacity Pressure Score", capacity_pressure)

st.markdown("---")

# ---------------------------------------------------
# OPERATIONAL ALERT ENGINE
# ---------------------------------------------------

st.header("Operational Alert Engine")

alert_col1, alert_col2, alert_col3 = st.columns(3)

with alert_col1:
    if capacity_pressure >= 80:
        st.error("Critical Capacity Pressure Detected")
    elif capacity_pressure >= 60:
        st.warning("High Capacity Pressure")
    else:
        st.success("Capacity Pressure Stable")

with alert_col2:
    if icu_utilization >= 85:
        st.error("ICU Strain Detected")
    elif icu_utilization >= 70:
        st.warning("Moderate ICU Utilization")
    else:
        st.success("ICU Utilization Stable")

with alert_col3:
    if avg_ed_wait >= 90:
        st.error("Severe ED Congestion")
    elif avg_ed_wait >= 60:
        st.warning("ED Congestion Warning")
    else:
        st.success("ED Flow Stable")

st.markdown("---")

# ---------------------------------------------------
# COMMAND CENTER STATUS SUMMARY
# ---------------------------------------------------

st.header("Command Center Status Summary")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.info("System Scope: Enterprise Hospital Operations")

with status_col2:
    st.success("Monitoring Status: Active")

with status_col3:
    st.warning("Decision Layer: Executive Operations Intelligence")

st.markdown("---")
# ---------------------------------------------------
# VISUAL ANALYTICS
# ---------------------------------------------------

st.header("Enterprise Operational Analytics")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if "hospital_unit" in df.columns and "length_of_stay_days" in df.columns:
        los_by_unit = (
            df.groupby("hospital_unit")["length_of_stay_days"]
            .mean()
            .reset_index()
            .sort_values("length_of_stay_days", ascending=False)
        )

        fig_los = px.bar(
            los_by_unit,
            x="hospital_unit",
            y="length_of_stay_days",
            title="Average Length of Stay by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "length_of_stay_days": "Average LOS (Days)"
            }
        )

        st.plotly_chart(fig_los, use_container_width=True)

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
            title="Capacity Pressure Score by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "capacity_pressure_score": "Capacity Pressure Score"
            }
        )

        st.plotly_chart(fig_pressure, use_container_width=True)

    
# ---------------------------------------------------
# ADVANCED OPERATIONAL VISUALS
# ---------------------------------------------------

st.header("Advanced Operational Intelligence")

adv_col1, adv_col2 = st.columns(2)

with adv_col1:
    if "ed_wait_time_minutes" in df.columns:
        fig_ed = px.histogram(
            df,
            x="ed_wait_time_minutes",
            nbins=30,
            title="Emergency Department Wait Time Distribution",
            labels={"ed_wait_time_minutes": "ED Wait Time (Minutes)"}
        )

        st.plotly_chart(fig_ed, use_container_width=True, key="ed_wait_distribution")

with adv_col2:
    if "icu_flag" in df.columns and "hospital_unit" in df.columns:
        icu_by_unit = (
            df.groupby("hospital_unit")["icu_flag"]
            .sum()
            .reset_index()
            .sort_values("icu_flag", ascending=False)
        )

        fig_icu = px.bar(
            icu_by_unit,
            x="hospital_unit",
            y="icu_flag",
            title="ICU Patient Volume by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "icu_flag": "ICU Patient Count"
            }
        )

        st.plotly_chart(fig_icu, use_container_width=True, key="icu_volume_chart")

adv_col3, adv_col4 = st.columns(2)

with adv_col3:
    if "length_of_stay_days" in df.columns:
        fig_los_dist = px.histogram(
            df,
            x="length_of_stay_days",
            nbins=30,
            title="Length of Stay Distribution",
            labels={"length_of_stay_days": "Length of Stay (Days)"}
        )

        st.plotly_chart(fig_los_dist, use_container_width=True, key="los_distribution_chart")

with adv_col4:
    if "hospital_unit" in df.columns and "total_cost_usd" in df.columns:
        cost_by_unit = (
            df.groupby("hospital_unit")["total_cost_usd"]
            .sum()
            .reset_index()
            .sort_values("total_cost_usd", ascending=False)
        )

        fig_cost = px.bar(
            cost_by_unit,
            x="hospital_unit",
            y="total_cost_usd",
            title="Operational Cost by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "total_cost_usd": "Total Cost (USD)"
            }
        )

        st.plotly_chart(fig_cost, use_container_width=True, key="cost_by_unit_chart")

st.markdown("---")

# ---------------------------------------------------
# EXECUTIVE OVERVIEW
# ---------------------------------------------------

st.header("Executive Operational Overview")

st.write(
    """
    This system provides enterprise-level healthcare operations intelligence
    focused on patient flow, hospital capacity, ICU utilization,
    emergency department congestion, workflow analytics,
    and executive operational monitoring.
    """
)

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------

st.header("Operational Dataset Preview")

st.dataframe(df.head())

# ---------------------------------------------------
# ENTERPRISE FOOTER
# ---------------------------------------------------

st.markdown("---")

st.markdown(
    """
    <div style='padding-top: 10px; padding-bottom: 20px;'>

    <h4 style='color:#0f172a; margin-bottom:0px;'>
    Enterprise Healthcare Operations Intelligence System
    </h4>

    <p style='color:#475569; font-size:16px; margin-top:8px;'>
    Executive Hospital Workflow, Capacity & Operational Analytics
    </p>

    <hr style='margin-top:15px; margin-bottom:15px;'>

    <p style='font-size:15px; color:#334155; line-height:1.8;'>

    <strong>Built & Deployed by Dr. Samuel Israel</strong><br>

    Healthcare Data Scientist • Digital Health Transformation Specialist •
    Healthcare Operations Intelligence • Executive Healthcare BI •
    Healthcare AI & Predictive Analytics •
    ML Engineering & Deployable AI Systems •
    Clinical & Operational Intelligence Systems

    </p>

    </div>
    """,
    unsafe_allow_html=True
)