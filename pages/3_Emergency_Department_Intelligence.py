import streamlit as st
import plotly.express as px

from utils.data_loader import load_hospital_data
from utils.filters import apply_global_filters

st.set_page_config(
    page_title="Emergency Department Intelligence",
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
st.title("Emergency Department Intelligence")
st.subheader("ED Wait Times, Congestion Monitoring & Emergency Workflow Analytics")

st.markdown("---")

st.header("ED Operations Overview")

col1, col2, col3 = st.columns(3)

with col1:
    if "ed_wait_time_minutes" in df.columns:
        avg_wait = round(df["ed_wait_time_minutes"].mean(), 2)
        st.metric("Average ED Wait Time", f"{avg_wait} mins")

with col2:
    if "ed_wait_time_minutes" in df.columns:
        max_wait = round(df["ed_wait_time_minutes"].max(), 2)
        st.metric("Maximum ED Wait Time", f"{max_wait} mins")

with col3:
    if "ed_wait_time_minutes" in df.columns:
        high_wait_cases = df[df["ed_wait_time_minutes"] >= 60].shape[0]
        st.metric("High Wait-Time Cases", f"{high_wait_cases:,}")

st.markdown("---")

st.header("ED Congestion Intelligence")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if "ed_wait_time_minutes" in df.columns:
        fig_wait_dist = px.histogram(
            df,
            x="ed_wait_time_minutes",
            nbins=30,
            title="ED Wait Time Distribution",
            labels={"ed_wait_time_minutes": "ED Wait Time (Minutes)"}
        )

        st.plotly_chart(fig_wait_dist, use_container_width=True, key="ed_wait_dist_page")

with chart_col2:
    if "hospital_unit" in df.columns and "ed_wait_time_minutes" in df.columns:
        ed_wait_by_unit = (
            df.groupby("hospital_unit")["ed_wait_time_minutes"]
            .mean()
            .reset_index()
            .sort_values("ed_wait_time_minutes", ascending=False)
        )

        fig_wait_unit = px.bar(
            ed_wait_by_unit,
            x="hospital_unit",
            y="ed_wait_time_minutes",
            title="Average ED Wait Time by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "ed_wait_time_minutes": "Average ED Wait Time"
            }
        )

        st.plotly_chart(fig_wait_unit, use_container_width=True, key="ed_wait_by_unit_page")

st.markdown("---")

st.header("ED Operational Risk Signals")

risk_col1, risk_col2, risk_col3 = st.columns(3)

with risk_col1:
    if "ed_wait_time_minutes" in df.columns:
        if avg_wait >= 90:
            st.error("Severe ED Congestion")
        elif avg_wait >= 60:
            st.warning("Moderate ED Congestion")
        else:
            st.success("ED Flow Stable")

with risk_col2:
    if "ed_wait_time_minutes" in df.columns:
        if high_wait_cases > 100:
            st.error("High Wait-Time Burden Detected")
        elif high_wait_cases > 50:
            st.warning("Moderate Wait-Time Burden")
        else:
            st.success("Wait-Time Burden Controlled")

with risk_col3:
    st.info("ED monitoring supports patient flow, triage efficiency, and congestion control.")

st.markdown("---")

st.header("Operational Interpretation")

st.write(
    """
    This page provides emergency department congestion intelligence, including ED
    wait-time patterns, high wait-time burden, and unit-level congestion signals.
    These insights support operational teams in monitoring patient flow delays,
    identifying bottlenecks, and improving emergency department throughput.
    """
)