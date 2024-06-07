import os
import socket
import sys

from flops_utils.logging import logger

SERVER_PORT = os.environ.get("PROJECT_OBSERVER_PORT")

# NOTE: This python server cannot bind to this service's RR IP.
# What works is if it listens to 0.0.0.0 and the clients connect to this RR IP only.
SERVER_IP = "0.0.0.0"


def handle_oak_service_communication() -> None:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, int(SERVER_PORT)))

    server_socket.listen(1)
    logger.info("Project Observer started")
    sys.stdout.flush()

    while True:
        client_socket, _ = server_socket.accept()  # _ = client_address
        data = client_socket.recv(1024)
        if data:
            message = data.decode("utf-8")
            logger.info(message)

            response = "Message received: " + message
            client_socket.send(response.encode("utf-8"))

        client_socket.close()
        sys.stdout.flush()
