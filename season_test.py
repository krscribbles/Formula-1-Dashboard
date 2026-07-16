import fastf1
import pandas as pd

schedule = fastf1.get_event_schedule(2025)

all_results = []

for _, race in schedule.iloc[1:].iterrows():

    race_name = race["EventName"]

    print(f"Loading {race_name}")

    session = fastf1.get_session(
        2025,
        race_name,
        "R"
    )

    session.load()

    year = session.event["EventDate"].year
    track = session.event["Location"]

    for driver_number in session.drivers:

        driver_info = session.get_driver(driver_number)

        all_results.append({
            "Driver": driver_info["FullName"],
            "Team": driver_info["TeamName"],
            "Year": year,
            "Race": race_name,
            "Track": track,
            "GridPosition": driver_info["GridPosition"],
            "FinishPosition": driver_info["Position"],
            "Points": driver_info["Points"]
        })

historical_df = pd.DataFrame(all_results)

print(historical_df.shape)
print(historical_df.head())