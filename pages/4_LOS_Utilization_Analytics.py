import streamlit as st
import plotly.express as px

from utils.data_loader import load_hospital_data
from utils.filters import apply_global_filters

st.set_page_config(
    page_title="LOS & Utilization Analytics",
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

st.title("LOS & Utilization Analytics")
st.subheader("Length of Stay, Prolonged Stay Burden & Operational Efficiency Intelligence")

st.markdown("---")

st.header("LOS Performance Overview")

col1, col2, col3 = st.columns(3)

with col1:
    if "length_of_stay_days" in df.columns:
        avg_los = round(df["length_of_stay_days"].mean(), 2)
        st.metric("Average LOS", f"{avg_los} days")

with col2:
    if "length_of_stay_days" in df.columns:
        median_los = round(df["length_of_stay_days"].median(), 2)
        st.metric("Median LOS", f"{median_los} days")

with col3:
    if "length_of_stay_days" in df.columns:
        prolonged_cases = df[df["length_of_stay_days"] >= 7].shape[0]
        st.metric("Prolonged Stay Cases", f"{prolonged_cases:,}")

st.markdown("---")

st.header("Utilization Intelligence")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if "length_of_stay_days" in df.columns:
        fig_los = px.histogram(
            df,
            x="length_of_stay_days",
            nbins=30,
            title="Length of Stay Distribution",
            labels={"length_of_stay_days": "Length of Stay (Days)"}
        )

        st.plotly_chart(fig_los, use_container_width=True, key="los_distribution_page")

with chart_col2:
    if "hospital_unit" in df.columns and "length_of_stay_days" in df.columns:
        los_by_unit = (
            df.groupby("hospital_unit")["length_of_stay_days"]
            .mean()
            .reset_index()
            .sort_values("length_of_stay_days", ascending=False)
        )

        fig_los_unit = px.bar(
            los_by_unit,
            x="hospital_unit",
            y="length_of_stay_days",
            title="Average LOS by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "length_of_stay_days": "Average LOS"
            }
        )

        st.plotly_chart(fig_los_unit, use_container_width=True, key="los_by_unit_page")

st.markdown("---")

st.header("Operational Efficiency Signals")

eff_col1, eff_col2, eff_col3 = st.columns(3)

with eff_col1:
    if "length_of_stay_days" in df.columns:
        if avg_los >= 10:
            st.error("High LOS Burden")
        elif avg_los >= 7:
            st.warning("Moderate LOS Burden")
        else:
            st.success("LOS Performance Stable")

with eff_col2:
    if "length_of_stay_days" in df.columns:
        if prolonged_cases > 100:
            st.error("High Prolonged-Stay Burden")
        elif prolonged_cases > 50:
            st.warning("Moderate Prolonged-Stay Burden")
        else:
            st.success("Prolonged Stay Controlled")

with eff_col3:
    st.info("LOS analytics supports throughput, discharge planning, and utilization efficiency.")

st.markdown("---")

st.header("Operational Interpretation")

st.write(
    """
    This page provides length-of-stay and utilization intelligence for hospital
    operations. It highlights average LOS, prolonged-stay burden, and unit-level
    utilization patterns. These insights support operational teams in improving
    throughput, discharge planning, bed availability, and workflow efficiency.
    """
)