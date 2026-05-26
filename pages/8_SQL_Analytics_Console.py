import streamlit as st
import duckdb

from utils.data_loader import load_hospital_data
from utils.filters import apply_global_filters


st.set_page_config(
    page_title="SQL Analytics Console",
    layout="wide"
)

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

df = apply_global_filters(df)

st.title("SQL Analytics Console")
st.subheader("Live SQL-Powered Healthcare Operations Intelligence")

st.markdown("---")

st.info(
    """
    This page enables SQL-style operational analytics directly against the hospital
    operations dataset. It demonstrates SQL analytics maturity, executive KPI querying,
    and healthcare operational reporting capability.
    """
)

# Register dataframe as SQL table
conn = duckdb.connect()
conn.register("hospital_operations_dataset", df)

st.header("Prebuilt Executive SQL Queries")

query_options = {
    "Operational KPI Summary": """
SELECT
    COUNT(*) AS total_encounters,
    ROUND(AVG(length_of_stay_days), 2) AS average_los,
    ROUND(AVG(ed_wait_time_minutes), 2) AS average_ed_wait_time,
    ROUND(AVG(capacity_pressure_score), 2) AS average_capacity_pressure,
    ROUND(SUM(total_cost_usd), 2) AS total_operational_cost
FROM hospital_operations_dataset;
""",

    "Capacity Pressure by Unit": """
SELECT
    hospital_unit,
    ROUND(AVG(capacity_pressure_score), 2) AS average_capacity_pressure,
    COUNT(*) AS patient_volume
FROM hospital_operations_dataset
GROUP BY hospital_unit
ORDER BY average_capacity_pressure DESC;
""",

    "LOS Analytics by Unit": """
SELECT
    hospital_unit,
    ROUND(AVG(length_of_stay_days), 2) AS average_los,
    COUNT(*) AS patient_volume
FROM hospital_operations_dataset
GROUP BY hospital_unit
ORDER BY average_los DESC;
""",

    "ED Congestion by Unit": """
SELECT
    hospital_unit,
    ROUND(AVG(ed_wait_time_minutes), 2) AS average_ed_wait_time,
    COUNT(*) AS patient_volume
FROM hospital_operations_dataset
GROUP BY hospital_unit
ORDER BY average_ed_wait_time DESC;
""",

    "Financial Operations by Unit": """
SELECT
    hospital_unit,
    ROUND(SUM(total_cost_usd), 2) AS total_operational_cost,
    ROUND(AVG(total_cost_usd), 2) AS average_encounter_cost,
    COUNT(*) AS patient_volume
FROM hospital_operations_dataset
GROUP BY hospital_unit
ORDER BY total_operational_cost DESC;
""",

    "ICU Utilization by Unit": """
SELECT
    hospital_unit,
    SUM(icu_flag) AS icu_cases,
    COUNT(*) AS total_cases,
    ROUND((SUM(icu_flag) * 100.0 / COUNT(*)), 2) AS icu_utilization_rate
FROM hospital_operations_dataset
GROUP BY hospital_unit
ORDER BY icu_utilization_rate DESC;
"""
}

selected_query = st.selectbox(
    "Select Executive SQL Query",
    list(query_options.keys())
)

sql_query = st.text_area(
    "SQL Query",
    value=query_options[selected_query],
    height=260
)

if st.button("Run SQL Query"):
    try:
        result = conn.execute(sql_query).df()

        st.success("SQL query executed successfully.")
        st.dataframe(result, use_container_width=True)

    except Exception as e:
        st.error(f"SQL execution error: {e}")

st.markdown("---")

st.header("Executive Interpretation")

st.write(
    """
    The SQL Analytics Console strengthens the system by enabling structured
    operational querying across hospital workflow, capacity, LOS, ED congestion,
    ICU utilization, and financial operations. This demonstrates healthcare SQL
    analytics capability beyond dashboard visualization.
    """
)