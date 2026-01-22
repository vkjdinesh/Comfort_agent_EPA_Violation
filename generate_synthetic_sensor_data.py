# generate_synthetic_sensor_data.py

import csv
import random
from datetime import datetime, timedelta

OUTPUT_FILE = "synthetic_sensor_data.csv"
TOTAL_SAMPLES = 6000  

ROOMS = {
    "living_room": {
        "temperature": (13, 35),
        "humidity": (80, 85),
    },
    "bedroom": {
        "temperature": (13, 35),
        "humidity": (45, 85), 
    },
    "kitchen": {
        "temperature": (12, 35),
        "humidity": (50, 85),
    },
}

START_TIME = datetime(2025, 1, 1, 0, 0, 0)


def generate_value(min_val, max_val):
    return round(random.uniform(min_val, max_val), 2)


def generate_dataset():
    current_time = START_TIME
    time_step = timedelta(minutes=1)

    rows = []

    while len(rows) < TOTAL_SAMPLES:
        for room, sensors in ROOMS.items():
            for sensor, (min_v, max_v) in sensors.items():
                rows.append([
                    current_time.strftime("%Y-%m-%d %H:%M:%S"),
                    room,
                    sensor,
                    generate_value(min_v, max_v)
                ])

                if len(rows) >= TOTAL_SAMPLES:
                    break
            if len(rows) >= TOTAL_SAMPLES:
                break

        current_time += time_step

    return rows


def save_to_csv(data):
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "room", "sensor_name", "value"])
        writer.writerows(data)

    print(f"✅ Generated {len(data)} samples → {OUTPUT_FILE}")


if __name__ == "__main__":
    dataset = generate_dataset()
    save_to_csv(dataset)
