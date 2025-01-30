import json
import sys
import time

import numpy
import pandas as pd
import requests
from datasets import load_dataset
from flops_utils.logging import logger
from icecream import ic

model_server_service_ip = sys.argv[1]

if not model_server_service_ip:
    logger.fatal("Please provide a proper 'Model Server Service IP' e.g. ~ 10.30.X.Y '")
    sys.exit(1)


mnist = load_dataset("mnist", trust_remote_code=True)

while True:
    logger.info("Picking a random sample from the MNIST dataset for inference checking")
    random_image_index = numpy.random.randint(0, len(mnist["train"]))
    image_info = mnist["train"][random_image_index]

    image_data = image_info["image"]
    label = image_info["label"]
    logger.info(f"Label of the random test sample: '{label}'")

    image_array = numpy.array(image_data)
    flattened_image_data = image_array.flatten()
    df = pd.DataFrame([flattened_image_data])
    csv_data = df.to_csv(index=False)

    logger.info("Sending inference request to the trained model container")
    headers = {"Content-Type": "text/csv"}
    response = requests.post(
        f"http://{model_server_service_ip}:8080/invocations",
        headers=headers,
        data=csv_data,
    )
    ic(response)

    logger.info(f"Inference result: '{response.text}'")

    inference_result = json.loads(response.text)["predictions"][0]

    original_expected_label = label
    ic(original_expected_label == inference_result)

    time.sleep(5)
