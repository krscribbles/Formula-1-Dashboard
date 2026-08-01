import sqlite3
import pandas as pd

DB_NAME = "f1_live_data.db"

with sqlite3.connect(DB_NAME) as conn:
    print("Loading historical results...")
    df = pd.read_sql("SELECT * FROM historical_results", conn)
    print(f"Loaded {len(df)} rows.")

    # Standardize driver names
    df["Driver"] = df["Driver"].replace({"Kimi Antonelli": "Andrea Kimi Antonelli"})

    # Positions gained for valid race finishes
    valid_df = df[(df["GridPosition"] > 0) & (df["FinishPosition"] > 0)].copy()
    valid_df["PositionsGained"] = valid_df["GridPosition"] - valid_df["FinishPosition"]

    # Filter drivers with >= 10 valid races
    gained_stats = (
        valid_df.groupby("Driver")
        .filter(lambda x: len(x) >= 10)
        .groupby("Driver")["PositionsGained"]
        .mean()
        .rename("AvgPositionsGained")
    )

    # Base Driver Stats
    print("Generating driver statistics...")
    driver_stats = df.groupby("Driver").agg(
        Races=("Race", "count"),
        AvgGrid=("GridPosition", "mean"),
        AvgFinish=("FinishPosition", "mean"),
        TotalPoints=("Points", "sum"),
        Wins=("FinishPosition", lambda x: (x == 1).sum()),
        Podiums=("FinishPosition", lambda x: (x <= 3).sum())
    ).reset_index()

    # Get latest team per driver
    latest_team = df.sort_values("Year").drop_duplicates(subset=["Driver"], keep="last")[["Driver", "Team"]]
    
    # Merge additional metrics
    driver_stats = driver_stats.merge(latest_team, on="Driver", how="left")
    driver_stats = driver_stats.merge(gained_stats, on="Driver", how="left")
    driver_stats["AvgPositionsGained"] = driver_stats["AvgPositionsGained"].fillna(0)

    # Driver Percentages & Metrics
    driver_stats["WinPercentage"] = driver_stats["Wins"] / driver_stats["Races"] * 100
    driver_stats["PodiumPercentage"] = driver_stats["Podiums"] / driver_stats["Races"] * 100
    driver_stats["ExpectedFinish"] = driver_stats["AvgFinish"]
    driver_stats["WinProbability"] = driver_stats["WinPercentage"].clip(0, 100)
    driver_stats["PodiumProbability"] = driver_stats["PodiumPercentage"].clip(0, 100)

    driver_stats["PerformanceScore"] = (
        driver_stats["TotalPoints"] * 0.45 +
        (100 - driver_stats["AvgFinish"] * 5) * 0.25 +
        driver_stats["WinPercentage"] * 0.15 +
        driver_stats["PodiumPercentage"] * 0.10 +
        (driver_stats["AvgPositionsGained"] + 10) * 0.5
    )

    driver_cols = [
        "Driver", "Team", "Races", "AvgGrid", "AvgFinish", "TotalPoints",
        "Wins", "Podiums", "AvgPositionsGained", "WinPercentage",
        "PodiumPercentage", "ExpectedFinish", "WinProbability",
        "PodiumProbability", "PerformanceScore"
    ]
    driver_stats = driver_stats[driver_cols].round(2)

    # Constructor Stats
    print("Generating constructor statistics...")
    constructor_stats = df.groupby("Team").agg(
        Races=("Race", "count"),
        AvgGrid=("GridPosition", "mean"),
        AvgFinish=("FinishPosition", "mean"),
        TotalPoints=("Points", "sum"),
        Wins=("FinishPosition", lambda x: (x == 1).sum()),
        Podiums=("FinishPosition", lambda x: (x <= 3).sum())
    ).reset_index()

    constructor_stats["WinPercentage"] = constructor_stats["Wins"] / constructor_stats["Races"] * 100
    constructor_stats["PodiumPercentage"] = constructor_stats["Podiums"] / constructor_stats["Races"] * 100
    constructor_stats = constructor_stats.round(2)

    # Export to CSV & SQL
    driver_stats.to_csv("driver_stats.csv", index=False)
    constructor_stats.to_csv("constructor_stats.csv", index=False)

    driver_stats.to_sql("driver_stats", conn, if_exists="replace", index=False)
    constructor_stats.to_sql("constructor_stats", conn, if_exists="replace", index=False)

print("✓ driver_stats.csv created")
print("✓ constructor_stats.csv created")
print("✓ SQLite tables updated")
print("\nDone!")