import sqlite3
import pandas as pd

with sqlite3.connect("f1_live_data.db") as conn:
    # Clean driver names once
    df = pd.read_sql("SELECT * FROM historical_results", conn)
    df["Driver"] = df["Driver"].replace({"Andrea Kimi Antonelli": "Kimi Antonelli"})
    df.to_sql("historical_results", conn, if_exists="replace", index=False)

    # Aggregate stats directly in SQL
    query = """
    SELECT 
        Driver,
        Team,
        COUNT(*) AS Races,
        AVG(GridPosition) AS AvgGrid,
        AVG(FinishPosition) AS AvgFinish,
        SUM(Points) AS TotalPoints,
        SUM(CASE WHEN FinishPosition <= 3 THEN 1 ELSE 0 END) AS Podiums,
        SUM(CASE WHEN FinishPosition = 1 THEN 1 ELSE 0 END) AS Wins,
        AVG(GridPosition - FinishPosition) AS AvgPositionsGained
    FROM historical_results
    GROUP BY Driver, Team
    ORDER BY TotalPoints DESC
    """
    stats = pd.read_sql(query, conn)

# Percentages
stats["WinPercentage"] = (stats["Wins"] / stats["Races"] * 100).round(2)
stats["PodiumPercentage"] = (stats["Podiums"] / stats["Races"] * 100).round(2)

# Performance score
stats["PerformanceScore"] = (
    stats["TotalPoints"] * 0.40
    + stats["WinPercentage"] * 2.0
    + stats["PodiumPercentage"] * 1.2
    + stats["AvgPositionsGained"] * 10
    - stats["AvgFinish"] * 5
).round(2)

# Normalization & expectations
max_score, min_score = stats["PerformanceScore"].max(), stats["PerformanceScore"].min()
stats["ExpectedFinish"] = (
    20 - ((stats["PerformanceScore"] - min_score) / (max_score - min_score)) * 19
).round(1)

# Probabilities
prob_base = 100 - stats["ExpectedFinish"] * 5
stats["PodiumProbability"] = (stats["PodiumPercentage"] * 0.7 + prob_base * 0.3).clip(0, 100).round(1)
stats["WinProbability"] = (stats["WinPercentage"] * 0.7 + prob_base * 0.3).clip(0, 100).round(1)

# Sort and export
stats = stats.sort_values(by="PerformanceScore", ascending=False)

with sqlite3.connect("f1_live_data.db") as conn:
    stats.to_sql("driver_stats", conn, if_exists="replace", index=False)

stats.to_csv("driver_stats.csv", index=False)
df.to_csv("historical_results.csv", index=False)