# EPA Comfort Monitoring System 

## **EPA Standards**
| Parameter | Safe Zone | Violation |
|-----------|-----------|-----------|
| Temperature | **20–24°C** | &lt;20°C or &gt;24°C |
| Humidity | **≤60%** | &gt;60% |

**Light Colors:**
- **RED**  = HIGH severity (H&gt;75% or extreme temps)
- **YELLOW**  = MEDIUM severity  
- **GREEN** = Safe zone

## **System Architecture**

SensorAgent → ComfortAgent → ActuatorAgent


## 🚀 **Quick Start**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run agents (3 terminals)
python sensor_agent2.py        #  Sensors
python comfort Agent_ver2.py #  EPA Monitor  
python Actuator_Agent_Comfort.py #  Lights

