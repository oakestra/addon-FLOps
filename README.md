# FLOps Management
<img src="https://github.com/oakestra/plugin-FLOps-management/assets/65814168/c8ba7bce-634e-46a3-a62c-5c152b7f4829" alt="Description of image" width="50%" height="auto">

## FLOps Manager
The manager is responsible for:
- Serving the FLOps API (Entrypoint for FLOps processes/projects)
- Requesting/Managing FLOps components/services e.g. by delegating calls to Oakestra.
- Interacting with the FLOps DB for storing persistent data.
- Is connected to the FLOps MQTT Broker and can handle incoming messages.
  - E.g. if the FL Image Builder succeeds - start spawning the FL Aggregator and FL Learner.
  - If the Builder fails - log the specific error and handle the FLOps Project termination.


## FLOps MQTT Broker
A [Mosquitto MQTT Broker](https://mosquitto.org/) that enabled communication between the FLOps components deployed on Workers and the Manager.

## FLOps Image Registry
A [CNCF Distribution Registry](https://distribution.github.io/distribution/) that allows the FLOps Image Builder to store/push its images to and for the FL Learners to pull them.

## FLOps DB
- Stores persistent data relevant to FLOps via MongoDB.
- All connected FLOps components that are part of the same FLOps project need to be able to identify and recall each other if need be.
- E.g. Once the FLOps Image Builder finishes building it calls the FLOps Manager to continue with the next FLOps Project steps. Including the undeployment of the current Builder service and spawning the Aggregator and Learners. To do so the Manager needs the FLOps ProjectID to retrieve the necessary details of the Builder and to initiate the upcoming components. These details (mostly IDs) are stored in the FLOps DB.

## MLflow MLOps 
TODO/WIP
