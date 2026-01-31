import pandas as pd
import numpy as np
import os

LOG_PATH = "output/db_activity_logs.csv"
OUTPUT_PATH = "output/PS2_Anomaly_Report.csv"
os.makedirs("output", exist_ok=True)

if not os.path.exists(LOG_PATH):
    raise FileNotFoundError(f"Input file not found: {LOG_PATH}. Please run generate_db_activity_logs.py first.")

df = pd.read_csv(LOG_PATH)


baselines = (
    df.groupby("user")["rows_scanned"]
      .agg(["mean", "std"])
      .reset_index()
      .rename(columns={"mean": "avg_rows", "std": "std_rows"})
)

df = df.merge(baselines, on="user", how="left")


df["z_score"] = np.where(
    df["std_rows"] == 0, 
    0, 
    (df["rows_scanned"] - df["avg_rows"]) / df["std_rows"]
)
df["deviation_strength"] = df["z_score"].abs()


df["risk_percentile"] = df["deviation_strength"].rank(pct=True)

df["risk_score"] = pd.qcut(
    df["risk_percentile"],
    q=[0.0, 0.7, 0.9, 1.0],
    labels=["LOW", "MEDIUM", "HIGH"]
)


df["flagged"] = df["risk_score"].isin(["MEDIUM", "HIGH"])


df["reason"] = (
    "User baseline average rows ≈ " + df["avg_rows"].round(0).astype(str) +
    ". Current query scanned " + df["rows_scanned"].astype(str) +
    " rows, indicating deviation from learned normal behavior."
)


final = df[[
    "timestamp",
    "user",
    "role",
    "query_type",
    "table",
    "rows_scanned",
    "avg_rows",
    "z_score",
    "risk_percentile",
    "risk_score",
    "flagged",
    "reason"
]]

final.to_csv(OUTPUT_PATH, index=False)

print("PS-2 anomaly report generated (no rule-based logic).")
