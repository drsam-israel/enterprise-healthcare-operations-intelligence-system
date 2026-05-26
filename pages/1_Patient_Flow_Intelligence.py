import streamlit as st
import plotly.express as px

from utils.data_loader import load_hospital_data
from utils.filters import apply_global_filters

st.set_page_config(
    page_title="Patient Flow Intelligence",
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
st.title("Patient Flow Intelligence")
st.subheader("Enterprise Workflow, Admissions, Discharges & Transfer Analytics")

st.markdown("---")

st.header("Patient Flow Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Patient Encounters", f"{len(df):,}")

with col2:
    if "transfer_count" in df.columns:
        avg_transfers = round(df["transfer_count"].mean(), 2)
        st.metric("Average Transfers per Patient", avg_transfers)

with col3:
    if "length_of_stay_days" in df.columns:
        avg_los = round(df["length_of_stay_days"].mean(), 2)
        st.metric("Average LOS", f"{avg_los} days")

st.markdown("---")

st.header("Workflow Movement Analytics")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if "hospital_unit" in df.columns:
        unit_volume = (
            df["hospital_unit"]
            .value_counts()
            .reset_index()
        )
        unit_volume.columns = ["hospital_unit", "patient_volume"]

        fig_unit = px.bar(
            unit_volume,
            x="hospital_unit",
            y="patient_volume",
            title="Patient Volume by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "patient_volume": "Patient Volume"
            }
        )

        st.plotly_chart(fig_unit, use_container_width=True, key="patient_volume_by_unit")

with chart_col2:
    if "transfer_count" in df.columns:
        fig_transfer = px.histogram(
            df,
            x="transfer_count",
            nbins=20,
            title="Transfer Count Distribution",
            labels={"transfer_count": "Transfer Count"}
        )

        st.plotly_chart(fig_transfer, use_container_width=True, key="transfer_distribution")

st.markdown("---")

st.header("Operational Interpretation")

st.write(
    """
    This page evaluates patient movement across the hospital system, including
    unit-level volume, transfer burden, and workflow efficiency. These metrics
    support operational leaders in identifying bottlenecks, patient flow delays,
    and areas requiring workflow optimization.
    """
)