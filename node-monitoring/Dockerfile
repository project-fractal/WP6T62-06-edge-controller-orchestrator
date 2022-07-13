ARG PYTHON_VERSION=3.9.13

FROM python:${PYTHON_VERSION}

RUN useradd -ms /bin/bash edgemonitor

USER edgemonitor
WORKDIR /home/edgemonitor

COPY --chown=edgemonitor:edgemonitor requirements.txt /home/edgemonitor/requirements.txt
COPY --chown=edgemonitor:edgemonitor nodes.txt /home/edgemonitor/nodes.txt
COPY --chown=edgemonitor:edgemonitor nodemonitoring.py /home/edgemonitor/nodemonitoring.py

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT python3 nodemonitoring.py
