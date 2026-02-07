import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    database="product-analytics-pipeline",
    user="postgres",
    password="Ishashah23$"
)

cur = conn.cursor()

with open("events.json") as f:
    for line in f:
        e = json.loads(line)
        cur.execute(
            """
            INSERT INTO events_raw VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                e["event_id"],
                e["user_id"],
                e["event_type"],
                e["timestamp"],
                e["device"],
                e["country"],
                e["amount"]
            )
        )

conn.commit()
cur.close()
conn.close()
