# Home Automation Agent

The Home Automation Agent system consists of four interconnected agents that collaboratively control smart lighting based on environmental sensor data.

*The Sensor Agent* reads synthetic sensor data (temperature, humidity) from a CSV file every 15 seconds, determines appropriate light colors for each room, and publishes these decisions over MQTT.

*The Light Controller Agent* receives sensor commands and feedback, logs them, and forwards light commands to the actuator.

*The Actuator Agent* waits for approval from the LLM Supervisor Agent, which reviews commands using AI-based validation and rule checks before execution.

Once approved, the actuator executes the commands on physical lights and reports status back to the supervisor.

The entire system runs concurrently, orchestrated by a master script, with all MQTT communication standardized through a shared base class.

This modular and cyclical architecture ensures automated and responsive control of home lighting based on environmental conditions.

## System Flow
```
Sensor Agent analyzing... → publishes light commands
↓
Light Controller receives → forwards to actuator commands
↓
Actuator receives → AWAITING supervisor → pending status
↓
LLM reviewing... → approved/warning → feedback
↓
Actuator EXECUTING → physical lights → completed status
↓
Loop repeats every 15 seconds (Sensor Agent cycle)
```

### Sensor Agent

1. Periodically reads synthetic sensor data from a CSV file.
2. Decides light colors for each room based on temperature and humidity.
3. Publishes these decisions as JSON messages over MQTT to the Light Controller Agent.
4. Creates an MQTT-based processing loop by regularly publishing both decisions and raw measurements to a predefined topic.

### Light Controller Agent

1. Subscribes to sensor commands and supervisor feedback.
2. Logs incoming decisions.
2. Immediately forwards them unchanged (with timestamp) to home/agents/actuator-commands for physical light execution.

### LLM Supervisor Agent

1. Subscribes to actuator status reports.
2. Uses Qwen LLM to validate execution based on rules and AI reasoning.
3. Publishes approval, warning, or rejection feedback with a 100-second timeout protection.

### Actuator Agent

1. Receives light commands.
2. Awaits LLM supervisor approval.
3. Executes approved commands on physical lights.

### Orchestrator

Launches all four agents concurrently to run the complete home automation pipeline.

### MQTT Base

Provides a standardized Paho MQTT client setup and connection management as the base class for all four agents.


### Running the System

1. Create a virtual environment.  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
3. Configure the local LLM path if necessary.
4. Run the agents: 
    ```bash
    python orchestrator.py

### Task Description 
As a continuation of the Home Automation Agent project, build a Comfort Agent to detect Environmental Protection Agency (EPA) violations. This agent can be either a custom implementation or use an LLM.
Example safe zone criteria:
```
Temperature: 20–24 °C
Humidity: ≤ 60%
```
Note: The flow is as follows:
Sensor Agent → Comfort Agent (LLM or custom) → EPA alert