FROM ubuntu:21.10

RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt-get install -y tzdata
RUN apt-get install glances -y

RUN useradd -ms /bin/bash metricsexporter

USER metricsexporter
WORKDIR /home/metricsexporter

EXPOSE 61208

COPY glances.conf /etc/glances/glances.conf

ENTRYPOINT glances -w 
