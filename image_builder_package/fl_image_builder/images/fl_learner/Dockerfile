ARG BASE_IMAGE
FROM ${BASE_IMAGE}

RUN conda clean -tipy
WORKDIR /fl_learner
RUN mv /fl_base/* /fl_learner/ && rm -r /fl_base
COPY . /fl_learner

