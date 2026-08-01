import fastf1
import pandas as pd
import sqlite3

# Load session data
session = fastf1.get_session(2025, "British Grand Prix", "R")
session.load()

# Parse driver data
driver_data = [
    {
        "Driver": d["FullName"],
        "Team": d["TeamName"],
        "Year": session.event["EventDate"].year,
        "Race": session.event["EventName"],
        "Track": session.event["Location"],
        "GridPosition": d["GridPosition"],
        "FinishPosition": d["Position"],
        "Points": d["Points"],
    }
    for d in (session.get_driver(num) for num in session.drivers)
]

df = pd.DataFrame(driver_data)

# Save to SQLite & verify
with sqlite3.connect("f1_live_data.db") as conn:
    df.to_sql("historical_results", conn, if_exists="replace", index=False)
    print(pd.read_sql("SELECT * FROM historical_results", conn))