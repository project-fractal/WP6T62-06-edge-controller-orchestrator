ARG PYTHON_VERSION=3.9.13

FROM python:${PYTHON_VERSION}

RUN useradd -ms /bin/bash resource-manager

USER resource-manager
WORKDIR /home/resource-manager

COPY --chown=resource-manager:resource-manager utils /home/resource-manager/utils
COPY --chown=resource-manager:resource-manager requirements.txt /home/resource-manager/requirements.txt
COPY --chown=resource-manager:resource-manager nodes.yaml /home/resource-manager/nodes.yaml
COPY --chown=resource-manager:resource-manager resource_manager.py /home/resource-manager/resource_manager.py

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT python3 resource_manager.py
