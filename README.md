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


#############


TODO  update readme

# FLOps Project Components
<img src="https://github.com/oakestra/plugin-FLOps-project-components/assets/65814168/40cccf6c-25fc-437d-bae4-7f799b7f326c" alt="Description of image" width="50%" height="auto">

A FLOps Project is a logical unit that groups together all related FLOps components that are necessary to fulfill a concrete user FLOps request.
A Project enabled its components to find and communicate with each other.

E.g. A user wants to run FLOps on his provided ML repo. All following processes that get triggered due to these initial requests are part of one FLOps project.
Another call will lead to a different FLOps project.

Thus supporting multiple FLOps projects and components running at the same time - i.e. serving multiple user FL requests at the same time.</br>

## FL (Learner) Image Builder
- Is instantiated if the requested FL Learner Image is not found in the FLOps Image Registry.
- Builds the FL Learner Image to be able to create FL Learners (also called FL Clients) and pushes the resulting image to the FLOps image registry.
- This FL Learner image is based on the user-provided ML repo/code which gets wrapped into an FL-compatible image including all necessary dependencies for proper training.

## FLOps UI
- Enables the user/developer to easily inspect the current progress of his FLOps processes/project.
- Depending on the use case a non-developer user will not be able to see other components but the UI to abstract away technical details and complexities.
- Every FLOps component has the capability to send a message to the UI (via internal Oakestra service networking), including the FLOps manager (which uses MQTT, because the manager is not deployed as a service).

## FLOps Aggregator
- The FL Server that aggregates the Learner updates.

## FL Learner
- The FL Client that trains the model and sends its updates ot the aggregator.
