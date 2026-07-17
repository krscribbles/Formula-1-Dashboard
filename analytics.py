import sqlite3
import pandas as pd

conn = sqlite3.connect("f1_live_data.db")

df = pd.read_sql(
    "SELECT * FROM historical_results",
    conn
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

print(check_stats.head())
print(check_stats.shape)