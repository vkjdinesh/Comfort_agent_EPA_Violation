# comfort_agent_final.py - 100% RELIABLE EPA MONITOR
import json
import time
from base.mqtt_base import MQTTBaseAgent

EPA_ALERT_TOPIC = "home/agents/epa-alerts"
SENSOR_TOPIC = "home/agents/light-commands"

class ComfortAgent(MQTTBaseAgent):
    def __init__(self):
        super().__init__("comfort")
        self.client.on_message = self.on_message

    def subscribe_to_topics(self):
        self.connect()
        self.client.subscribe(SENSOR_TOPIC, qos=1)
        print(" ComfortAgent EPA monitor ready!")

    def check_epa(self, temps, humids):
        """EPA Standards: Temp 20-24°C, Humidity ≤60%"""
        violations = []
        for room, temp in temps.items():
            humidity = humids.get(room)
            if humidity is None: continue
            
            issues = []
            if not 20 <= temp <= 24:
                issues.append(f"T{temp:.1f}°C")
            if humidity > 60:
                issues.append(f"H{humidity:.1f}%")
                
            if issues:
                violations.append({
                    "room": room,
                    "reason": f"EPA violation: {'+'.join(issues)}",
                    "temp": temp,
                    "humidity": humidity,
                    "severity": "HIGH" if humidity > 75 or temp < 18 or temp > 26 else "MEDIUM"
                })
        return violations

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            temps = data["sensors"]["temps"]
            humids = data["sensors"]["humids"]
        except:
            return

        print(f"\n  Temps: {temps}")
        print(f"  Humids: {humids}")

        violations = self.check_epa(temps, humids)
        
        alert = {
            "agent": "comfort",
            "timestamp": time.time(),
            "violations": violations,
            "status": "ALERT" if violations else "OK"
        }

        if violations:
            print(" EPA VIOLATIONS DETECTED:")
            for v in violations:
                print(f"  {v['room']}: {v['reason']} ({v['severity']})")
        else:
            print(" All rooms EPA compliant")

        self.client.publish(EPA_ALERT_TOPIC, json.dumps(alert), qos=1)
        print(f" Alert → {EPA_ALERT_TOPIC}")

    def run(self):
        self.subscribe_to_topics()
        print(" EPA ComfortAgent monitoring...")
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("\n Stopped")
        finally:
            self.disconnect()

if __name__ == "__main__":
    ComfortAgent().run()
