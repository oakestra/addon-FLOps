ARG BASE_IMAGE
FROM ${BASE_IMAGE}
LABEL org.opencontainers.image.source https://github.com/oakestra/addon-flops

COPY . /fl_base
WORKDIR /fl_base
