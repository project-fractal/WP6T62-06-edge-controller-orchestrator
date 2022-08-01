#! /bin/bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker build -t resource_manager .
docker run -d --network=host resource_manager
