ARG PYTHON_VERSION=3.9.13

FROM python:${PYTHON_VERSION}

RUN useradd -ms /bin/bash custom-orchestrator

USER custom-orchestrator
WORKDIR /home/custom-orchestrator

COPY --chown=custom-orchestrator:custom-orchestrator utils /home/custom-orchestrator/utils
COPY --chown=custom-orchestrator:custom-orchestrator requirements.txt /home/custom-orchestrator/requirements.txt
COPY --chown=custom-orchestrator:custom-orchestrator custom-orchestrator.py /home/custom-orchestrator/custom-orchestrator.py

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT python3 custom-orchestrator.py