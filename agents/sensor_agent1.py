from base.mqtt_base import MQTTBaseAgent
import csv
from pathlib import Path
import time
import json
'''
A sensor agent periodically reads synthetic sensor data from a CSV file, 
decides light colors for each room based on temperature and humidity, 
and publishes these decisions as JSON messages over MQTT to a light controller agent. 
This creates an MQTT-based processing loop where the agent derives 
room-level environmental status from CSV data and regularly publishes both decisions and 
raw measurements to a predefined topic.
'''
CSV_PATH = Path(r"Synthetic_sensor_data.csv")
LIGHT_COMMANDS_TOPIC = "home/agents/light-commands"

class SensorAgent(MQTTBaseAgent):
    def __init__(self):
        super().__init__("sensor")
    
    def subscribe_to_topics(self):
        self.connect()
        print("SensorAgent subscribed!")
    
    def read_sensors(self):  
        temps = {}
        humids = {}  
        try:
            with CSV_PATH.open("r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["sensor_name"] == "temperature":
                        temps[row["room"]] = float(row["value"])
                    elif row["sensor_name"] == "humidity":  
                        humids[row["room"]] = float(row["value"])
        except Exception as e:
            print(f"CSV error: {e}")
        return temps, humids
    
    def decide_lights(self, temps, humids): 
        decisions = {}
        for room in temps:  
            temp = temps[room]
            humid = humids.get(room, 0) 
            #Based on the context of your assignment you can set the rule here
            if temp < 15 or temp > 30:
                color = "red"      
            elif humid > 80:
                color = "yellow"   
            else:
                color = "green"   
            
            # Show both values in log
            print(f" {room}: {temp:.1f}°C ({humid:.1f}%) → {color}")
            decisions[room] = color
        return decisions
    
    def run(self):
        try:
            while True:
                print("\n SensorAgent analyzing...")
                temps, humids = self.read_sensors()      
                decisions = self.decide_lights(temps, humids) 
                
                payload = json.dumps({
                    "from": "sensor",
                    "timestamp": time.time(),
                    "light_commands": decisions,
                    "sensors": {"temps": temps, "humids": humids}  
                })
                
                self.client.publish(LIGHT_COMMANDS_TOPIC, payload, qos=1)
                print(f" MQTT → LightController: {decisions}")
                
                time.sleep(15)
        except KeyboardInterrupt:
            print("\n SensorAgent stopped")
        finally:
            self.disconnect()
