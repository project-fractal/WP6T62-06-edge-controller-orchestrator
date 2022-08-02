#! /bin/bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker build -t custom-orchestrator .
docker run -d --network=host custom-orchestrator