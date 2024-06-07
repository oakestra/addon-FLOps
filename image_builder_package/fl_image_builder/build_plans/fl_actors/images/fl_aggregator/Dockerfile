ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ARG USE_DEVEL_BASE_IMAGES="false"
RUN if [ "$USE_DEVEL_BASE_IMAGES" = "false" ]; then\
        pip install \
            # Note: These dependency versions do not yet exist in conda.
            paho-mqtt==2.0 \
            && conda install -y \
            mlflow>=2.12.1 \
            psutil>=5.9.8 \
            pynvml>=11.5.0 &&\
        conda clean -tipy \
    ; fi

WORKDIR /fl_aggregator
RUN mv /fl_base/* /fl_aggregator/ && rm -r /fl_base
COPY . /fl_aggregator
