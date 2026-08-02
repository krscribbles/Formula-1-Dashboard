# Formula 1 Live Analytics & Predictive Dashboard

An end-to-end Formula 1 data pipeline and interactive Power BI dashboard that pulls live race and championship data from an API, processes it in Python, stores it in SQLite, and transforms it into a scannable analytics layer for standings, head-to-head comparisons, position gains, and lightweight race predictions.

---

## Why this project exists

Formula 1 data is rich, but it is often fragmented across timing sheets, standings tables, race summaries, and broadcast graphics. That makes it difficult to answer practical questions such as:

- Who is gaining the most positions relative to grid?
- Which drivers are consistently outperforming their teammates?
- How do constructor trends change across the season?
- What does current form suggest about the next race?

This project solves that by creating a single, repeatable analytics pipeline with a dashboard built for both F1 fans and data analysts.

---

## Problem Statement / Real-World Utility

| Problem | Real-World Utility |
|---|---|
| F1 data is spread across multiple tables and sources | Creates a single source of truth for live championship analysis |
| Broadcast visuals are static and event-focused | Adds reusable, interactive reporting across races and seasons |
| Raw results do not show racecraft clearly | Tracks positions gained, average finish, podiums, and teammate gaps |
| Future performance is hard to estimate from standings alone | Adds simple predictive scoring for win/podium/finish outlooks |
| Manual analysis is slow and inconsistent | Automates extraction, transformation, storage, and refresh |

---

## Project Overview

| Component | Description |
|---|---|
| **Data Extraction** | Pulls live and historical F1 data from the Jolpica / Ergast API |
| **Processing** | Cleans, transforms, and enriches data using Python, Pandas, and NumPy |
| **Storage** | Persists structured data in SQLite for repeatable analysis |
| **Analytics Layer** | Prepares aggregated metrics for downstream reporting |
| **Visualization** | Presents the final model in Power BI Desktop with interactive filters and DAX measures |

---

## Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **SQLite3**
- **Power BI Desktop**
- **DAX**
- **Jolpica / Ergast F1 API**

---

## Architecture

```text
API (Jolpica / Ergast)
        |
        v
Python ETL Scripts
        |
        v
SQLite Database (f1_live_data.db)
        |
        v
Analytics / Aggregation Layer
        |
        v
CSV Exports / Reporting Tables
        |
        v
Power BI Dashboard (.pbix)
```

---

## Key Features

| Feature / Module | What it does | Output |
|---|---|---|
| **Driver Standings** | Tracks live points, wins, rank movement, and driver filters | Championship view by driver |
| **Constructor Standings** | Summarizes team points, team form, and comparative performance | Constructor leaderboard |
| **Teammate Head-to-Head** | Compares drivers within the same team across key performance metrics | Side-by-side comparison matrix |
| **Position Gain Analysis** | Measures grid recovery and race-day position changes | Position gain / loss insights |
| **Live Overview** | Shows current leaders, completed races, and active standings context | Quick championship snapshot |
| **Predictive Race Insights** | Produces lightweight performance scores and probability-based estimates | Win / podium / expected finish view |

---

## Dashboard Modules

| Module | Purpose | Example Metrics |
|---|---|---|
| **Championship Standings** | Monitor title fight progression | Points, wins, rank, delta movement |
| **Driver Comparison** | Compare two drivers directly | Wins, podiums, average finish, net gain |
| **Constructor Analysis** | Evaluate team performance | Team points, average finishing position, head-to-head split |
| **Position Gain Analysis** | Identify racecraft and recovery patterns | Positions gained, positions lost, net change |
| **Predictive Insights** | Estimate future race outcomes | Performance score, podium probability, expected finish |

---

## Repository Layout

| File / Folder | Purpose |
|---|---|
| `season_loader.py` | Loads season data from the API and populates the database |
| `analytics.py` | Builds aggregated tables and derived metrics for reporting |
| `generate_stats.py` | Generates analytical outputs and dashboard-ready datasets |
| `f1_live_data.db` | SQLite database containing processed F1 data |
| `Dashboard.pbix` | Power BI report file for the interactive dashboard |
| `requirements.txt` | Python dependencies for the data pipeline |
| `README.md` | Project overview and setup instructions |
| `Images` | Project overview and visual dashboard |


---

## Screenshot Preview

| Image 1 | Image 2 |
|---|---|
| `![Driver Standings](<img width="4000" height="2233" alt="image" src="https://github.com/user-attachments/assets/4ccc61a0-b4f9-4171-83d9-25f813a45c91" />
)` | `![Constructor Analysis](<img width="4000" height="2229" alt="image" src="https://github.com/user-attachments/assets/7c34f5d5-6773-4c99-bde5-9a15a34231ac" />
)` |
| `![Driver Comparison](<img width="4000" height="2219" alt="image" src="https://github.com/user-attachments/assets/9d27b76d-13cf-4192-9003-fff3d3c8a5bd" />
)` | `![Predictive Insights](<img width="3987" height="2240" alt="image" src="https://github.com/user-attachments/assets/e2e16203-7b55-4014-bfdc-38956207ff45" />
)` |



---

## How It Works

1. The Python scripts call the Jolpica / Ergast API.
2. Race, driver, and constructor data is cleaned and normalized.
3. Metrics are stored in SQLite for repeatable querying.
4. Aggregated outputs are exported for BI consumption.
5. Power BI loads the data model and renders the dashboard.
6. DAX measures power the filters, comparisons, and live-style reporting.

---

## Getting Started

### 1) Clone the repository

````powershell
git clone https://github.com/krscribbles/Formula-1-Dashboard.git
cd Formula-1-Dashboard
