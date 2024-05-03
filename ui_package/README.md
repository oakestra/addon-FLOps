# plugins-FLOps-UI
The FLOps UI image is used for observing the FLOps processes/project.
It is intended to inform the user/dev about the successful or failed FLOps processes like FL Learner image builder progress, etc.

This image comes with two communication "channels":
- A python socket based one that is intended for Oakestra-service-internal communication. It uses the Oakestra Network and can be reached e.g. by using this service's RR IP.
- A MQTT one that subscribes to the FLOps Manager MQTT broker. This one is necessary to be able to receive messages from the FLOps Manager which is not deployed as an Oakestra service.

TODO: The image can be found in the Oakestra image registry: `ghcr.io/oakestra/plugins/flops/fl-ui:latest`

## Input Params Explanation
Input arguments for the python module ```python main.py ...```
    1. FLOps ID - Unique identifier that is created during the FLOps Manager API call for a new FL project.
        - e.g. `123456`
    2. IP of the FLOps Manager MQTT Broker
        - e.g. `192.168.178.44`
    3. Port of the FLOps Manager MQTT Broker
        - e.g. `9027`
