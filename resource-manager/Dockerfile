ARG PYTHON_VERSION=3.9.13

FROM python:${PYTHON_VERSION}

RUN useradd -ms /bin/bash resource_manager

USER resource_manager
WORKDIR /home/resource_manager

COPY --chown=resource_manager:resource_manager utils /home/resource_manager/utils
COPY --chown=resource_manager:resource_manager requirements.txt /home/resource_manager/requirements.txt
COPY --chown=resource_manager:resource_manager nodes.yaml /home/resource_manager/resource_manager/nodes.yaml
COPY --chown=resource_manager:resource_manager resource_manager.py /home/resource_manager/resource_manager.py

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT python3 resource_manager.py
