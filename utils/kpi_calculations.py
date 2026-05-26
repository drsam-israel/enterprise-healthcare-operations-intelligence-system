def calculate_total_admissions(df):
    return df.shape[0]


def calculate_avg_los(df):
    if "length_of_stay_days" in df.columns:
        return round(df["length_of_stay_days"].mean(), 2)
    return 0


def calculate_icu_utilization(df):
    if "icu_flag" in df.columns:
        icu_patients = df[df["icu_flag"] == 1].shape[0]
        total_patients = df.shape[0]

        if total_patients > 0:
            return round((icu_patients / total_patients) * 100, 2)

    return 0


def calculate_avg_ed_wait(df):
    if "ed_wait_time_minutes" in df.columns:
        return round(df["ed_wait_time_minutes"].mean(), 2)
    return 0


def calculate_total_operational_cost(df):
    if "total_cost_usd" in df.columns:
        return round(df["total_cost_usd"].sum(), 2)
    return 0


def calculate_avg_capacity_pressure(df):
    if "capacity_pressure_score" in df.columns:
        return round(df["capacity_pressure_score"].mean(), 2)
    return 0