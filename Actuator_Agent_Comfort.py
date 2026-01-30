# actuator_agent.py - Controls lights based on EPA violations
import json
import time
from base.mqtt_base import MQTTBaseAgent

EPA_ALERT_TOPIC = "home/agents/epa-alerts"
LIGHT_CONTROL_TOPIC = "home/agents/light-commands"

class ActuatorAgent(MQTTBaseAgent):
    def __init__(self):
        super().__init__("actuator")
        self.current_lights = {}  # Track light states per room
        self.client.on_message = self.on_message

    def subscribe_to_topics(self):
        self.connect()
        self.client.subscribe(EPA_ALERT_TOPIC, qos=1)
        print("✅ ActuatorAgent subscribed to EPA alerts!")

    def get_light_color(self, violation):
        """Map EPA severity to light colors"""
        severity = violation.get("severity", "MEDIUM")
        
        if severity == "HIGH":
            return "red"      # 🚨 Critical violation
        elif severity == "MEDIUM":
            return "yellow"   # ⚠️  Warning
        else:
            return "green"    # ✅ Safe

    def update_room_light(self, room, color):
        """Send light command for a room"""
        light_command = {room: color}
        
        payload = json.dumps({
            "from": "actuator",
            "timestamp": time.time(),
            "light_commands": light_command,
            "reason": f"EPA {color.upper()} alert"
        })
        
        self.client.publish(LIGHT_CONTROL_TOPIC, payload, qos=1)
        print(f"💡 {room}: {color.upper()} light ON")

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode("utf-8"))
            violations = data.get("violations", [])
            
            if not violations:
                print("✅ No violations - all lights GREEN")
                # Default safe state for all known rooms
                for room in self.current_lights:
                    self.update_room_light(room, "green")
                return
            
            print(f"\n🚨 Processing {len(violations)} EPA violations...")
            
            # Process each violation
            for violation in violations:
                room = violation["room"]
                severity = violation.get("severity", "MEDIUM")
                reason = violation["reason"]
                color = self.get_light_color(violation)
                
                print(f"   {room}: {severity} - {reason}")
                self.update_room_light(room, color)
                self.current_lights[room] = color
                
        except Exception as e:
            print(f"❌ Actuator error: {e}")

    def run(self):
        self.subscribe_to_topics()
        print("🚀 ActuatorAgent ready - EPA → Lights!")
        print("HIGH=RED, MEDIUM=YELLOW, LOW=GREEN\n")
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("\n🛑 Actuator stopped")
        finally:
            self.disconnect()

if __name__ == "__main__":
    ActuatorAgent().run()
