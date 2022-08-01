import requests

import docker
import kubernetes
from docker.errors import APIError
from flask import Flask, request

from utils.logger import set_logger
from utils.constants import RESOURCE_LIST, PROTOCOL, API_BASE

logger = set_logger()


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


    # Program execution
if __name__ == '__main__':

    # Get nodes information from resource_manager at execution
    logger.info('Getting nodes information from resource-manager...')

    app = Flask(__name__)

    @app.route(API_BASE + 'update_taints', methods=['POST'])
    def do_your_thing():

        # Take actions on K8S and Docker accordingly:

        hostname = request.files['hostname']
        ip = request.files['ip']
        port = request.files['port']
        orchestrator = request.files['orchestrator']

        if orchestrator == 'kubernetes':
            pass
        # TODO: Take actions for Kubernetes

        elif orchestrator == 'docker':

            client = create_docker_client(ip=ip, port=2376)

        else:
            raise UnsupportedOrchestratorException(hostname, orchestrator)
