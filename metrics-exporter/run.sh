#! /bin/bash
docker run --name metrics-exporter -d --network=host --pid=host --hostname metricsexporter metrics-exporter
