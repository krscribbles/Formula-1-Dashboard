import fastf1
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Load a race session
session = fastf1.get_session(
    2025,
    "British Grand Prix",
    "R"
)

# Download and load the data
session.load()

race_name = session.event["EventName"]
track = session.event["Location"]
year = session.event["EventDate"].year


driver_data = []

for driver_number in session.drivers:

    driver_info = session.get_driver(driver_number)

    driver_data.append({
        "Driver": driver_info["FullName"],
        "Team": driver_info["TeamName"],
        "Year": year,
        "Race": race_name,
        "Track": track,
        "GridPosition": driver_info["GridPosition"],
        "FinishPosition": driver_info["Position"],
        "Points": driver_info["Points"]
    })

historical_df = pd.DataFrame(driver_data)


#sql

conn = sqlite3.connect("f1_live_data.db")

historical_df.to_sql(
    "historical_results",
    conn,
    if_exists="replace",
    index=False
)

test_df = pd.read_sql(
    "SELECT * FROM historical_results",
    conn
)

print(test_df)



