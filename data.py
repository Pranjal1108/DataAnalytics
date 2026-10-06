from pathlib import Path
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "noida_airport_data.csv"
FACILITIES = {
    "Phase 1": [("ATC Tower", "radio-tower"), ("Fire Station", "flame"), ("Hotels", "hotel"), ("Metro Link", "train-front")],
    "Phase 2": [("Additional Taxiways", "route"), ("Extended Terminal", "building-2"), ("Cargo Expansion", "package")],
    "Phase 3": [("2nd Runway", "plane-takeoff"), ("MRO Facility", "wrench"), ("Airport City Development", "building")],
    "Phase 4": [("3rd Runway", "plane-takeoff"), ("Intermodal Hub", "network"), ("Aerotropolis Expansion", "landmark")],
}

def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    numeric = ["Estimated_Cost_Cr", "Passenger_Capacity_MPPA", "Runways", "Terminal_Area_sqm", "Cargo_Area_sqm", "Area_Hectares"]
    required = set(numeric + ["Phase", "Year_Range", "Status"])
    if required - set(df.columns):
        raise ValueError(f"Missing columns: {sorted(required - set(df.columns))}")
    if df.Phase.tolist() != list(FACILITIES):
        raise ValueError("Expected Phase 1 through Phase 4 in order.")
    for column in numeric:
        df[column] = pd.to_numeric(df[column], errors="raise")
        if (df[column].dropna() < 0).any():
            raise ValueError(f"Negative values in {column}")
    if df[["Estimated_Cost_Cr", "Passenger_Capacity_MPPA"]].isna().any().any():
        raise ValueError("Cost and capacity are required.")
    if not df.Passenger_Capacity_MPPA.is_monotonic_increasing:
        raise ValueError("Cumulative capacity must not decrease.")
    df["Additional_Capacity_MPPA"] = df.Passenger_Capacity_MPPA.diff().fillna(df.Passenger_Capacity_MPPA)
    return df
