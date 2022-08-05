#! /bin/bash
docker rm $(docker ps -a -q)
docker build -t resource-manager .
docker run -d --network=host resource-manager
