# addon-FLOps-fl_image_builder
This repository hosts the code for the (static) FLOps fl-learner-image-builder image that is used to build the FL learner images needed for training.

This image does not only build the FL Learner image. It does the following:

NOTE: The image runs a python module to be able to handle complex logic easier.
1. Clones the GitHub repo provided via its URL.
2. Verifies if this repo is compatible.
    - Including checking necessary files.
3. Checks and handles dependencies to mitigate common errors.
    - This step cannot guarantee to fix every dependency issue.
4. Takes the cloned ML repo and augments it with necessary FL components.
5. Builds a FL Learner image for FL training including the provided dependencies.
6. Pushes the new image to an Oakestra docker registry.
7. Sends out messages to inform relevant components about the successful or failed image build and intermediate steps.

The image can be found in the Oakestra image registry.

## Commands
NOTE: Make sure you are in the `src` directory.

### Building the builder image
```
docker build -t ghcr.io/oakestra/addon-flops/image-builder:latest .
```

### Running the builder image (for testing if the image works)
```
docker run --privileged ghcr.io/oakestra/addon-flops/image-builder:latest python3 main.py https://github.com/Malyuk-A/mlflower-test-a https://192.168.178.44:5073 123456 192.168.178.44 9027 10.30.27.3
```
NOTE:
- The builder image will be used in the containerd environment of Oakestra so it is not the same as running it in a local privileged docker environment. 
    - However, this is the fastest way to check if the new image works as intended or not. 
    - I.e. if it does not work in a privileged local docker environment then it will most likely also not work anywhere else.
- After building the FL Learner image the builder container will try and push that new image to an Oakestra docker image registry container. If it does not exist yet or is out of your reach this step will fail.
    - The main purpose of this test run is to verify that the image can be built in the first place.

Input Params Explanation :

- --privileged : Needed to be able to build an image inside a container.
- Input arguments for the python module:
    1. GitHub ML repository URL
        - e.g. `https://github.com/Malyuk-A/mlflower-test-a`
    2. Target image registry URL
        - e.g. `https://192.168.178.44:5073`
    3. FLOps Project ID - Unique identifier that is created during the Root FL Manager API call for a new FL project.
        - e.g. `123456`
    4. IP of the FLOps Manager MQTT Broker
        - e.g. `192.168.178.44`
    6. IP of the corresponding FLOps UI service
        - e.g. `10.30.27.3`
        

### Pushing
```
docker push ghcr.io/oakestra/addon-flops/image-builder:latest
```


# Notes for Developers
I already tried to migrate this file structure to follow the other repos with the /package design using poetry.
This needs non-trivial, tricky refactoring so I leave it as is for now.
A few issues I faced: 
- poetry install requires more dev tooling than what is provided by the current slim base image.
    - Thus switching to a fuller image will lead to an explosion of the final image size.
    - This needs to be compensated by smart tool installation and removal or even multi-staged docker builds.
    - Even when just using a fuller image other novel error/exceptions pop up.
