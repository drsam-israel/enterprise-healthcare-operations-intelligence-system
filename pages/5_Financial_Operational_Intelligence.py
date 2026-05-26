import streamlit as st
import plotly.express as px

from utils.data_loader import load_hospital_data
from utils.filters import apply_global_filters

st.set_page_config(
    page_title="Financial & Operational Intelligence",
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

st.title("Financial & Operational Intelligence")
st.subheader("Operational Cost, Resource Utilization & Executive Healthcare Finance Analytics")

st.markdown("---")

st.header("Financial Operations Overview")

col1, col2, col3 = st.columns(3)

with col1:
    if "total_cost_usd" in df.columns:
        total_cost = df["total_cost_usd"].sum()
        st.metric("Total Operational Cost", f"${total_cost:,.0f}")

with col2:
    if "total_cost_usd" in df.columns:
        avg_cost = df["total_cost_usd"].mean()
        st.metric("Average Cost per Encounter", f"${avg_cost:,.0f}")

with col3:
    if "daily_cost_usd" in df.columns:
        avg_daily_cost = df["daily_cost_usd"].mean()
        st.metric("Average Daily Cost", f"${avg_daily_cost:,.0f}")

st.markdown("---")

st.header("Cost & Resource Utilization Analytics")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    if "hospital_unit" in df.columns and "total_cost_usd" in df.columns:
        cost_by_unit = (
            df.groupby("hospital_unit")["total_cost_usd"]
            .sum()
            .reset_index()
            .sort_values("total_cost_usd", ascending=False)
        )

        fig_cost_unit = px.bar(
            cost_by_unit,
            x="hospital_unit",
            y="total_cost_usd",
            title="Total Operational Cost by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "total_cost_usd": "Total Cost (USD)"
            }
        )

        st.plotly_chart(fig_cost_unit, use_container_width=True, key="cost_by_unit_financial")

with chart_col2:
    if "hospital_unit" in df.columns and "daily_cost_usd" in df.columns:
        daily_cost_by_unit = (
            df.groupby("hospital_unit")["daily_cost_usd"]
            .mean()
            .reset_index()
            .sort_values("daily_cost_usd", ascending=False)
        )

        fig_daily_cost = px.bar(
            daily_cost_by_unit,
            x="hospital_unit",
            y="daily_cost_usd",
            title="Average Daily Cost by Hospital Unit",
            labels={
                "hospital_unit": "Hospital Unit",
                "daily_cost_usd": "Average Daily Cost (USD)"
            }
        )

        st.plotly_chart(fig_daily_cost, use_container_width=True, key="daily_cost_by_unit_financial")

st.markdown("---")

st.header("Executive Cost Signals")

signal_col1, signal_col2, signal_col3 = st.columns(3)

with signal_col1:
    if "total_cost_usd" in df.columns:
        if avg_cost >= 15000:
            st.error("High Average Encounter Cost")
        elif avg_cost >= 10000:
            st.warning("Moderate Cost Pressure")
        else:
            st.success("Cost Performance Stable")

with signal_col2:
    if "icu_flag" in df.columns and "total_cost_usd" in df.columns:
        icu_cost = df[df["icu_flag"] == 1]["total_cost_usd"].sum()
        total_cost = df["total_cost_usd"].sum()

        if total_cost > 0:
            icu_cost_burden = round((icu_cost / total_cost) * 100, 2)
            st.metric("ICU Cost Burden", f"{icu_cost_burden}%")

with signal_col3:
    st.info("Financial intelligence supports cost control, capacity planning, and executive decision-making.")

st.markdown("---")

st.header("Operational Interpretation")

st.write(
    """
    This page provides executive-level financial and operational intelligence
    across hospital units. It highlights total cost, average encounter cost,
    daily cost patterns, ICU cost burden, and unit-level expenditure. These
    insights support healthcare leaders in monitoring operational efficiency,
    resource utilization, and financial sustainability.
    """
)