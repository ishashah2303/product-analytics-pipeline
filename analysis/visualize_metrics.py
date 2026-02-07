import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="product-analytics-pipeline",
    user="postgres",
    password="Ishashah23$"
)

# -----------------------------
# 1️⃣ Daily Conversion Rate
# -----------------------------
query_funnel_time = """
SELECT date, conversion_rate
FROM funnel_daily_metrics
ORDER BY date;
"""
df_time = pd.read_sql(query_funnel_time, conn)

plt.figure()
plt.plot(df_time["date"], df_time["conversion_rate"], marker="o")
plt.title("Daily Conversion Rate")
plt.xlabel("Date")
plt.ylabel("Conversion Rate (%)")
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -----------------------------
# 2️⃣ Funnel Breakdown
# -----------------------------
query_funnel = """
SELECT
    event_type,
    COUNT(DISTINCT user_id) AS users
FROM events_raw
GROUP BY event_type
ORDER BY users DESC;
"""
df_funnel = pd.read_sql(query_funnel, conn)

plt.figure()
plt.bar(df_funnel["event_type"], df_funnel["users"])
plt.title("User Funnel Breakdown")
plt.xlabel("Event Type")
plt.ylabel("Unique Users")
plt.tight_layout()
plt.show()

# -----------------------------
# 3️⃣ Conversion Rate by Device
# -----------------------------
query_device = """
SELECT device, conversion_rate
FROM device_metrics;
"""
df_device = pd.read_sql(query_device, conn)

plt.figure()
plt.bar(df_device["device"], df_device["conversion_rate"])
plt.title("Conversion Rate by Device")
plt.xlabel("Device")
plt.ylabel("Conversion Rate (%)")
plt.ylim(0, 100)
plt.tight_layout()
plt.show()

# -----------------------------
# 4️⃣ Retention and Cohort
# -----------------------------
query_cohort = """
SELECT cohort_date, day_n, retention_rate
FROM retention_cohort_daily
ORDER BY cohort_date, day_n;
"""
df = pd.read_sql(query_cohort, conn)

pivot = df.pivot(index="cohort_date", columns="day_n", values="retention_rate").fillna(0)

# Plot as an image (simple heatmap using matplotlib only)
plt.figure()
plt.imshow(pivot.values, aspect="auto")
plt.title("Cohort Retention Heatmap (Day N Retention %)")
plt.xlabel("Days Since First Activity (Day N)")
plt.ylabel("Cohort Date")
plt.xticks(range(len(pivot.columns)), [f"D{int(x)}" for x in pivot.columns])
plt.yticks(range(len(pivot.index)), [str(d) for d in pivot.index])
plt.colorbar(label="Retention Rate (%)")
plt.tight_layout()
plt.show()

conn.close()
