FROM python:3.10-slim
LABEL org.opencontainers.image.source https://github.com/oakestra/addon-flops

RUN apt-get update && \
    apt-get install -y wget &&\
    apt-get clean &&\
    wget -q https://github.com/distribution/distribution/releases/download/v2.8.3/registry_2.8.3_linux_amd64.tar.gz &&\
    tar -xvf registry_2.8.3_linux_amd64.tar.gz &&\
    mv registry /usr/local/bin/ &&\
    rm -rf registry_2.8.3_linux_amd64.tar.gz

COPY registry_config.yml /etc/docker/registry/config.yml
ENV REGISTRY_HTTP_ADDR=0.0.0.0:5073

WORKDIR /flops_image_registry
EXPOSE 5073

CMD ["registry", "serve", "/etc/docker/registry/config.yml"]
