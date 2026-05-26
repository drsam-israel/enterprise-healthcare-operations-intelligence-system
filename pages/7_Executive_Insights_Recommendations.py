import streamlit as st

from utils.data_loader import load_hospital_data
from utils.filters import apply_global_filters

st.set_page_config(
    page_title="Executive Insights & Recommendations",
    layout="wide"
)

df = load_hospital_data()

df = apply_global_filters(df)
# ---------------------------------------------------
# SIDEBAR
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

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("Executive Insights & Recommendations")

st.subheader(
    "Real-Time Operational Intelligence, Executive Risk Signals & Strategic Recommendations"
)

st.markdown("---")

# ---------------------------------------------------
# KPI EXTRACTION
# ---------------------------------------------------

avg_los = round(df["length_of_stay_days"].mean(), 2)

avg_ed_wait = round(df["ed_wait_time_minutes"].mean(), 2)

capacity_pressure = round(df["capacity_pressure_score"].mean(), 2)

total_cost = round(df["total_cost_usd"].sum(), 0)

icu_utilization = round(df["icu_flag"].mean() * 100, 2)

prolonged_cases = df[df["length_of_stay_days"] >= 7].shape[0]

high_wait_cases = df[df["ed_wait_time_minutes"] >= 60].shape[0]

# ---------------------------------------------------
# EXECUTIVE STATUS
# ---------------------------------------------------

st.header("Enterprise Operational Status")

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:
    st.metric("Average LOS", f"{avg_los} days")

with status_col2:
    st.metric("Average ED Wait", f"{avg_ed_wait} mins")

with status_col3:
    st.metric("Capacity Pressure", capacity_pressure)

st.markdown("---")

# ---------------------------------------------------
# EXECUTIVE INSIGHTS
# ---------------------------------------------------

st.header("Executive Operational Insights")

# LOS INSIGHT

if avg_los >= 8:

    st.error(
        f"""
        Elevated LOS burden detected across the enterprise environment.

        • Current Average LOS: {avg_los} days  
        • Prolonged Stay Cases: {prolonged_cases:,} patients

        Executive Impact:
        Reduced throughput efficiency, increased occupancy burden,
        and downstream ED congestion pressure.
        """
    )

# ED INSIGHT

if avg_ed_wait >= 60:

    st.warning(
        f"""
        Significant emergency department congestion identified.

        • Average ED Wait Time: {avg_ed_wait} minutes  
        • High Wait-Time Cases: {high_wait_cases:,}

        Executive Impact:
        Increased workflow bottlenecks, delayed patient movement,
        and elevated operational strain.
        """
    )

# CAPACITY INSIGHT

if capacity_pressure >= 60:

    st.warning(
        f"""
        Sustained hospital capacity pressure detected.

        • Capacity Pressure Score: {capacity_pressure}
        • ICU Utilization: {icu_utilization}%

        Executive Impact:
        Reduced operational flexibility and increased resource strain
        across high-acuity care environments.
        """
    )

# FINANCIAL INSIGHT

st.info(
    f"""
    Enterprise operational expenditure remains elevated.

    • Total Operational Cost: ${total_cost:,.0f}

    Executive Impact:
    Prolonged utilization patterns and ICU-intensive workflows
    are contributing to sustained operational expenditure pressure.
    """
)

st.markdown("---")

# ---------------------------------------------------
# EXECUTIVE RECOMMENDATIONS
# ---------------------------------------------------

st.header("Strategic Executive Recommendations")

recommendation_col1, recommendation_col2 = st.columns(2)

with recommendation_col1:

    st.success(
        """
        PRIORITY ACTIONS

        • Accelerate discharge planning workflows

        • Optimize ICU step-down transitions

        • Expand ED fast-track triage pathways

        • Strengthen enterprise bed coordination

        • Implement proactive occupancy escalation monitoring
        """
    )

with recommendation_col2:

    st.success(
        """
        STRATEGIC FOCUS AREAS

        • Throughput optimization

        • LOS reduction initiatives

        • Capacity strain mitigation

        • Workflow redesign & operational efficiency

        • Predictive operational preparedness
        """
    )

st.markdown("---")

# ---------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------

st.header("Executive Summary")

st.write(
    """
    The healthcare environment is currently operating under moderate-to-high
    operational strain driven by elevated LOS burden, sustained ED congestion,
    ICU resource intensity, and capacity pressure. Strategic focus should
    prioritize throughput optimization, discharge acceleration, workflow
    efficiency, and proactive operational planning.
    """
)

# ---------------------------------------------------
# FOOTER
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