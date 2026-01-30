from base.mqtt_base import MQTTBaseAgent
import csv
from pathlib import Path
import time
import json

"""
A sensor agent periodically reads synthetic sensor data from a CSV file,
decides light colors for each room based on temperature and humidity,
and publishes these decisions as JSON messages over MQTT.
"""

CSV_PATH = Path("Synthetic_sensor_data.csv")
LIGHT_COMMANDS_TOPIC = "home/agents/light-commands"


class SensorAgent(MQTTBaseAgent):
    def __init__(self):
        super().__init__("sensor")

    def read_sensors(self):
        temps = {}
        humids = {}

        try:
            with CSV_PATH.open("r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    room = row["room"]
                    value = float(row["value"])

                    if row["sensor_name"] == "temperature":
                        temps[room] = value
                    elif row["sensor_name"] == "humidity":
                        humids[room] = value

        except Exception as e:
            print(f"CSV error: {e}")

        return temps, humids

    def decide_lights(self, temps, humids):
        decisions = {}

        for room in temps:
            temp = temps[room]
            humid = humids.get(room, 0)

            if temp < 15 or temp > 30:
                color = "red"
            elif humid > 80:
                color = "yellow"
            else:
                color = "green"

            print(f"{room}: {temp:.1f}°C ({humid:.1f}%) → {color}")
            decisions[room] = color

        return decisions

    def run(self):
        # ✅ CONNECT TO MQTT BROKER
        self.connect()

        # ✅ START MQTT NETWORK LOOP (CRITICAL)
        self.client.loop_start()

        try:
            while True:
                print("\nSensorAgent analyzing...")

                temps, humids = self.read_sensors()
                decisions = self.decide_lights(temps, humids)

                payload = json.dumps({
                    "from": "sensor",
                    "timestamp": time.time(),
                    "light_commands": decisions,
                    "sensors": {
                        "temps": temps,
                        "humids": humids
                    }
                })

                result = self.client.publish(
                    LIGHT_COMMANDS_TOPIC,
                    payload,
                    qos=1
                )

                print("Publish result code:", result.rc)
                print(f"MQTT → {LIGHT_COMMANDS_TOPIC}")

                time.sleep(15)

        except KeyboardInterrupt:
            print("\nSensorAgent stopped")

        finally:
            self.client.loop_stop()
            self.disconnect()


if __name__ == "__main__":
    agent = SensorAgent()
    agent.run()
from base.mqtt_base import MQTTBaseAgent
import csv
from pathlib import Path
import time
import json

"""
A sensor agent periodically reads synthetic sensor data from a CSV file,
decides light colors for each room based on temperature and humidity,
and publishes these decisions as JSON messages over MQTT.
"""

CSV_PATH = Path("Synthetic_sensor_data.csv")
LIGHT_COMMANDS_TOPIC = "home/agents/light-commands"


class SensorAgent(MQTTBaseAgent):
    def __init__(self):
        super().__init__("sensor")

    def read_sensors(self):
        temps = {}
        humids = {}

        try:
            with CSV_PATH.open("r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    room = row["room"]
                    value = float(row["value"])

                    if row["sensor_name"] == "temperature":
                        temps[room] = value
                    elif row["sensor_name"] == "humidity":
                        humids[room] = value

        except Exception as e:
            print(f"CSV error: {e}")

        return temps, humids

    def decide_lights(self, temps, humids):
        decisions = {}

        for room in temps:
            temp = temps[room]
            humid = humids.get(room, 0)

            if temp < 15 or temp > 30:
                color = "red"
            elif humid > 80:
                color = "yellow"
            else:
                color = "green"

            print(f"{room}: {temp:.1f}°C ({humid:.1f}%) → {color}")
            decisions[room] = color

        return decisions

    def run(self):
        # ✅ CONNECT TO MQTT BROKER
        self.connect()

        # ✅ START MQTT NETWORK LOOP (CRITICAL)
        self.client.loop_start()

        try:
            while True:
                print("\nSensorAgent analyzing...")

                temps, humids = self.read_sensors()
                decisions = self.decide_lights(temps, humids)

                payload = json.dumps({
                    "from": "sensor",
                    "timestamp": time.time(),
                    "light_commands": decisions,
                    "sensors": {
                        "temps": temps,
                        "humids": humids
                    }
                })

                result = self.client.publish(
                    LIGHT_COMMANDS_TOPIC,
                    payload,
                    qos=1
                )

                print("Publish result code:", result.rc)
                print(f"MQTT → {LIGHT_COMMANDS_TOPIC}")

                time.sleep(15)

        except KeyboardInterrupt:
            print("\nSensorAgent stopped")

        finally:
            self.client.loop_stop()
            self.disconnect()


if __name__ == "__main__":
    agent = SensorAgent()
    agent.run()
