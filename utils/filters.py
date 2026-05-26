import streamlit as st


def apply_global_filters(df):
    st.sidebar.markdown("---")
    st.sidebar.subheader("Interactive Filters")

    filtered_df = df.copy()

    if "hospital_unit" in df.columns:
     units = ["All"] + sorted(df["hospital_unit"].dropna().unique())

    selected_unit = st.sidebar.selectbox(
        "Hospital Unit",
        options=units
    )

    if selected_unit != "All":
        filtered_df = filtered_df[filtered_df["hospital_unit"] == selected_unit]

    if "bed_occupancy_status" in df.columns:
     bed_status = ["All"] + sorted(df["bed_occupancy_status"].dropna().unique())

    selected_status = st.sidebar.selectbox(
        "Bed Status",
        options=bed_status
    )

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["bed_occupancy_status"] == selected_status
        ]

    if "icu_flag" in df.columns:
        icu_filter = st.sidebar.selectbox(
            "ICU Status",
            options=["All", "ICU Only", "Non-ICU Only"]
        )

        if icu_filter == "ICU Only":
            filtered_df = filtered_df[filtered_df["icu_flag"] == 1]
        elif icu_filter == "Non-ICU Only":
            filtered_df = filtered_df[filtered_df["icu_flag"] == 0]

    if "length_of_stay_days" in df.columns:
        min_los = float(df["length_of_stay_days"].min())
        max_los = float(df["length_of_stay_days"].max())

        los_range = st.sidebar.slider(
            "LOS Range (Days)",
            min_value=min_los,
            max_value=max_los,
            value=(min_los, max_los)
        )

        filtered_df = filtered_df[
            filtered_df["length_of_stay_days"].between(los_range[0], los_range[1])
        ]

    if "ed_wait_time_minutes" in df.columns:
        min_wait = float(df["ed_wait_time_minutes"].min())
        max_wait = float(df["ed_wait_time_minutes"].max())

        wait_range = st.sidebar.slider(
            "ED Wait Range (Minutes)",
            min_value=min_wait,
            max_value=max_wait,
            value=(min_wait, max_wait)
        )

        filtered_df = filtered_df[
            filtered_df["ed_wait_time_minutes"].between(wait_range[0], wait_range[1])
        ]

    return filtered_df