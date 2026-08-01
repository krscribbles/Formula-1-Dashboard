import os
import time
import sqlite3
import pandas as pd
import fastf1

DB_NAME = "f1_live_data.db"
TABLE_NAME = "historical_results"
YEARS = [2021, 2022, 2023, 2024, 2025]
MAX_RETRIES, RETRY_DELAY = 3, 30

os.makedirs("cache", exist_ok=True)
fastf1.cache.enable_cache("cache")


def init_db(conn):
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            Driver TEXT, Team TEXT, Year INTEGER, Race TEXT,
            Track TEXT, GridPosition INTEGER, FinishPosition INTEGER, Points REAL
        )
    """)


def season_exists(year, conn):
    try:
        res = pd.read_sql(f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE Year = ?", conn, params=(year,))
        return res.iloc[0, 0] > 0
    except Exception:
        return False


def load_season(year, conn):
    print(f"\n--- Loading {year} Season ---")
    if season_exists(year, conn):
        print(f"{year} already present in database.")
        return

    try:
        schedule = fastf1.get_event_schedule(year)
        races = schedule[(schedule["Session5"] == "Race") & (schedule["EventFormat"] != "testing")]
    except Exception as e:
        print(f"Couldn't fetch schedule for {year}: {e}")
        return

    season_results = []
    for race_no, (_, race) in enumerate(races.iterrows(), start=1):
        race_name = race["EventName"]
        print(f"[{race_no}/{len(races)}] {race_name}...", end=" ")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                session = fastf1.get_session(year, race_name, "R")
                session.load()
                track = session.event["Location"]

                season_results.extend([
                    {
                        "Driver": (d := session.get_driver(drv))["FullName"],
                        "Team": d["TeamName"],
                        "Year": year,
                        "Race": race_name,
                        "Track": track,
                        "GridPosition": d["GridPosition"],
                        "FinishPosition": d["Position"],
                        "Points": d["Points"],
                    }
                    for drv in session.drivers
                ])
                print("✓")
                break
            except Exception as e:
                if attempt == MAX_RETRIES:
                    print(f"Failed. Skipping.")
                else:
                    time.sleep(RETRY_DELAY)

    if season_results:
        df = pd.DataFrame(season_results)
        df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)
        print(f"Saved {len(df)} rows for {year}")


# Run Pipeline
start_time = time.time()
with sqlite3.connect(DB_NAME) as conn:
    init_db(conn)
    for year in YEARS:
        load_season(year, conn)

    final_df = pd.read_sql(f"SELECT * FROM {TABLE_NAME} ORDER BY Year, Race", conn)
    final_df.to_csv("historical_results.csv", index=False)

elapsed = (time.time() - start_time) / 60
print(f"\nImport Complete | Rows: {len(final_df)} | Time: {elapsed:.2f} mins")