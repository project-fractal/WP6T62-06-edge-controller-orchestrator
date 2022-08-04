ARG PYTHON_VERSION=3.9.13

FROM python:${PYTHON_VERSION}

RUN useradd -ms /bin/bash custom-orchestrator

COPY --chown=custom-orchestrator:custom-orchestrator utils /home/custom-orchestrator/utils
COPY --chown=custom-orchestrator:custom-orchestrator requirements.txt /home/custom-orchestrator/requirements.txt
COPY --chown=custom-orchestrator:custom-orchestrator custom_orchestrator.py /home/custom-orchestrator/custom_orchestrator.py

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /home/custom-orchestrator/requirements.txt

USER custom-orchestrator
WORKDIR /home/custom-orchestrator

ENV FLASK_APP=custom_orchestrator.py

ENTRYPOINT flask run --host=0.0.0.0 --port=9999
