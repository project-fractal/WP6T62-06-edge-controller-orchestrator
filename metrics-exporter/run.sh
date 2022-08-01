#! /bin/bash
docker run -d --network=host --pid=host --hostname metricsexporter metrics-exporter
