import sqlite3
import pandas as pd

conn = sqlite3.connect("f1_live_data.db")

df = pd.read_sql(
    "SELECT * FROM historical_results",
    conn
)

# Standardize driver names
df["Driver"] = df["Driver"].replace({
    "Andrea Kimi Antonelli": "Kimi Antonelli"
})

# Save the cleaned table back to SQLite
df.to_sql(
    "historical_results",
    conn,
    if_exists="replace",
    index=False
)

df = pd.read_sql(
    "SELECT * FROM historical_results",
    conn
)
# Standardize driver names
df["Driver"] = df["Driver"].replace({
    "Andrea Kimi Antonelli": "Kimi Antonelli"
})

# Overwrite the cleaned table
df.to_sql(
    "historical_results",
    conn,
    if_exists="replace",
    index=False
)

query = """
SELECT Driver,
       AVG(FinishPosition) AS AvgFinish
FROM historical_results
GROUP BY Driver
ORDER BY AvgFinish ASC
"""

avg_finish = pd.read_sql(query, conn)

query = """
SELECT Driver,
       COUNT(*) AS Races,
       AVG(GridPosition) AS AvgGrid,
       AVG(FinishPosition) AS AvgFinish,
       SUM(Points) AS TotalPoints
FROM historical_results
GROUP BY Driver
ORDER BY TotalPoints DESC
"""

driver_stats = pd.read_sql(query, conn)

query = """
SELECT Driver,
       COUNT(*) AS Podiums
FROM historical_results
WHERE FinishPosition <= 3
GROUP BY Driver
ORDER BY Podiums DESC
"""

podiums = pd.read_sql(query, conn)

query = """
SELECT Driver,
       COUNT(*) AS Wins
FROM historical_results
WHERE FinishPosition = 1
GROUP BY Driver
ORDER BY Wins DESC
"""

wins = pd.read_sql(query, conn)

final_stats = driver_stats.merge(
    podiums,
    on="Driver",
    how="left"
)

final_stats = final_stats.merge(
    wins,
    on="Driver",
    how="left"
)
final_stats["Wins"] = final_stats["Wins"].fillna(0)
final_stats["Podiums"] = final_stats["Podiums"].fillna(0)

query = """
SELECT Driver,
       AVG(GridPosition - FinishPosition) AS AvgPositionsGained
FROM historical_results
GROUP BY Driver
ORDER BY AvgPositionsGained DESC
"""

positions_gained = pd.read_sql(query, conn)

final_stats = final_stats.merge(
    positions_gained,
    on="Driver",
    how="left"
)

# Calculate percentages
final_stats["WinPercentage"] = (
    final_stats["Wins"] / final_stats["Races"] * 100
).round(2)

final_stats["PodiumPercentage"] = (
    final_stats["Podiums"] / final_stats["Races"] * 100
).round(2)

# Calculate Performance Score
final_stats["PerformanceScore"] = (
    final_stats["TotalPoints"] * 0.40 +
    final_stats["WinPercentage"] * 2.0 +
    final_stats["PodiumPercentage"] * 1.2 +
    final_stats["AvgPositionsGained"] * 10 -
    final_stats["AvgFinish"] * 5
).round(2)

# Expected Finish Position
max_score = final_stats["PerformanceScore"].max()
min_score = final_stats["PerformanceScore"].min()

final_stats["ExpectedFinish"] = (
    20 - (
        (final_stats["PerformanceScore"] - min_score)
        / (max_score - min_score)
    ) * 19
).round(1)

# Podium Probability
final_stats["PodiumProbability"] = (
    final_stats["PodiumPercentage"] * 0.7 +
    (100 - final_stats["ExpectedFinish"] * 5) * 0.3
).clip(0, 100).round(1)

# Win Probability
final_stats["WinProbability"] = (
    final_stats["WinPercentage"] * 0.7 +
    (100 - final_stats["ExpectedFinish"] * 5) * 0.3
).clip(0, 100).round(1)

# Sort by Performance Score
final_stats = final_stats.sort_values(
    by="PerformanceScore",
    ascending=False
)

final_stats.to_sql(
    "driver_stats",
    conn,
    if_exists="replace",
    index=False
)

check_stats = pd.read_sql(
    "SELECT * FROM driver_stats",
    conn
)

check_stats = pd.read_sql(
    "SELECT * FROM driver_stats",
    conn
)

final_stats.to_csv("driver_stats.csv", index=False)

historical_df = pd.read_sql(
    "SELECT * FROM historical_results",
    conn
)

historical_df.to_csv("historical_results.csv", index=False)