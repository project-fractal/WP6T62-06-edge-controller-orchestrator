import json
import requests
from ast import literal_eval

import docker
import kubernetes
from docker.errors import APIError
from flask import Flask, request

from utils.logger import set_logger
from utils.constants import RESOURCE_LIST, PROTOCOL, API_BASE

logger = set_logger()
app = Flask(__name__)


class UnsupportedOrchestratorException(Exception):
    def __init__(self, hostname, orchestrator):
        self.hostname = hostname
        self.orchestrator = orchestrator
        self.message = f'The Orchestrator {orchestrator} for node {hostname} is not supported'
        super().__init__(self.message)


def check_status(url, node):
    try:
        requests.get(url=url)
        return True

    except requests.exceptions.ConnectionError as e:
        logger.info(f'The connection was refused, is the node {node} alive?')
        logger.error(e)
        return False


def load_config():
    return


def create_docker_client(ip, port):
    # Create the Docker client instance
    try:
        env = {'DOCKER_HOST': f'{ip}:{port}'}
        docker_client = docker.client.from_env(environment=env)

        # Check the server responsiveness
        docker_client.ping()

        return docker_client

    except docker.errors.APIError as e:
        print(e)


def create_k8s_client():
    # TODO: Instantiate k8s client
    pass


# API ROUTES

@app.route('/', methods=['GET'])
# This route is called to check server's availability
def base():
    logger.info('Base method called')

    return 'Custom Orchestrator API OK'


@app.route(API_BASE + 'load_nodes', methods=['POST'])
# This route is called first and load the nodes information into a file to be used later to orchestrate
def load_nodes():
    logger.info('Getting nodes information from resource-manager...')
    nodes_test = request.json

    with open(file='./nodes.info', mode='w') as nodesconfig:
        nodesconfig.write(str(request.json))

    return 'Nodes config saved'


@app.route(API_BASE + 'update_taints', methods=['POST'])
# Read the nodes.info file and orchestrate according to tainted nodes.
def orchestrate():
    logger.info('Getting tainted nodes list from resource-manager...')

    # Read the nodes.info file as a dictionary
    with open(file='./nodes.info', mode='r') as nodesconfig:
        nodes_config_dict = literal_eval(nodesconfig.read())

    tainted_nodes = request.json

    # Take actions on K8S and Docker accordingly:

    for tainted_node in tainted_nodes:
        print(tainted_node)

    # if orchestrator == 'kubernetes':
    #     create_k8s_client(ip)
    # # TODO: Take actions for Kubernetes

    # elif orchestrator == 'docker':
    #     client = create_docker_client(ip=ip, port=2376)

    # else:
    #     raise UnsupportedOrchestratorException(hostname, orchestrator)

    return 'Taints and orchestration done'

    # Program execution
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=9999)
