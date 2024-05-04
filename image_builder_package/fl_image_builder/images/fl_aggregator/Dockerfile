ARG BASE_IMAGE
FROM ${BASE_IMAGE}

# Note: These dependency versions do not yet exist in conda.
RUN pip install \
    paho-mqtt==2.0 \
    icecream &&\
    conda install -y \
    mlflow>=2.12.1 \
    pydantic>=2.6.4 &&\
    conda clean -tipy

WORKDIR /fl_aggregator
RUN mv /fl_base/* /fl_aggregator/ && rm -r /fl_base
COPY . /fl_aggregator
