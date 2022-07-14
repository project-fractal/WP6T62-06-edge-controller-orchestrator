FROM ubuntu:22.10

RUN apt-get update && DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt-get install -y tzdata
RUN apt-get install glances -y

RUN useradd -ms /bin/bash edgecontroller

USER edgecontroller 
WORKDIR /home/edgecontroller

EXPOSE 61208

COPY glances.conf /etc/glances/glances.conCOPY glances.conf /etc/glances/glances.conff

ENTRYPOINT glances -w 
