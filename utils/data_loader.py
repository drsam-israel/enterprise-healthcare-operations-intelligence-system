import pandas as pd
from pathlib import Path


DATA_PATH = Path("data/hospital_operations_dataset.csv")


def load_hospital_data():
    """
    Load and prepare the hospital operations dataset.
    """

    df = pd.read_csv(DATA_PATH)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Convert date/time columns if they exist
    datetime_columns = [
        "admission_datetime",
        "discharge_datetime",
        "date",
        "admission_date",
        "discharge_date"
    ]

    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df