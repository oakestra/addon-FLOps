# FLOps Project Observer

The FLOps Project Observer is used for observing the FLOps processes/project.
It is intended to inform the user/dev about the successful or failed FLOps processes like FL Learner image builder progress, etc.

This component comes with two communication "channels":
- A Python-socket-based one that is intended for Oakestra-service-internal communication. It uses the Oakestra Network and can be reached e.g. by using this service's RR IP.
- A MQTT one that subscribes to the FLOps Manager MQTT broker. This one is necessary to be able to receive messages from the FLOps Manager which is not deployed as an Oakestra service.
