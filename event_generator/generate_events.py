import random
import uuid
from datetime import datetime,UTC
import json

EVENTS = ["view", "click", "add_to_cart", "purchase"]

def generate_event(user_id):
    event_type = random.choices(
        EVENTS,
        weights=[0.5, 0.3, 0.15, 0.05]
    )[0]

    return {
        "event_id": str(uuid.uuid4()),
        "user_id": user_id,
        "event_type": event_type,
        "timestamp": datetime.now(UTC).isoformat(),
        "device": random.choice(["web", "mobile"]),
        "country": random.choice(["US", "IN", "CA", "UK"]),
        "amount": round(random.uniform(10, 200), 2) if event_type == "purchase" else None
    }

def main():
    events = []
    for _ in range(1000):
        user_id = str(uuid.uuid4())
        for _ in range(random.randint(1, 10)):
            events.append(generate_event(user_id))

    with open("events.json", "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")

if __name__ == "__main__":
    main()
