import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("f1_live_data.db")

# Read data
query = """
SELECT Driver, Points
FROM drivers
ORDER BY Points DESC
"""

df = pd.read_sql(query, conn)

print(df)

# Create chart
plt.figure(figsize=(10,5))

plt.bar(
    df["Driver"],
    df["Points"]
)

plt.title("Points by Driver")
plt.xlabel("Driver")
plt.ylabel("Points")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()