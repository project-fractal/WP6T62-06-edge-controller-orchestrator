from ast import literal_eval

from flask import Flask, request

from utils.logger import set_logger
from utils.constants import API_BASE
from utils.check_taints import check_previous_taints

# Docker Orchestration
from utils.orchestrate_docker import orchestrate as docker_orchestrate
from utils.orchestrate_docker import create_client as create_docker_client

# K8S Orchestration
from utils.orchestrate_k8s import orchestrate as k8s_orchestrate
from utils.orchestrate_k8s import create_client as create_k8s_client

logger = set_logger()
app = Flask(__name__)


class UnsupportedOrchestratorException(Exception):
    def __init__(self, hostname, orchestrator):
        self.hostname = hostname
        self.orchestrator = orchestrator
        self.message = f'The Orchestrator {orchestrator} for node {hostname} is not supported'
        super().__init__(self.message)

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

    # TODO: Keep awareness of Tainted nodes and when untainted, remove restrictions
    tainted_nodes = request.json

    # Take actions on K8S and Docker accordingly:

    for tainted_node in tainted_nodes:
        logger.info(tainted_node +
                    ' is tainted. Applying custom orchestration...')

        if nodes_config_dict['orchestrator'][tainted_node] == 'kubernetes':
            # TODO: Take actions for Kubernetes
            k8s_client = create_k8s_client(
                nodes_config_dict['ips'][tainted_node])

            k8s_orchestrate(k8s_client)

        elif nodes_config_dict['orchestrator'][tainted_node] == 'docker':
            docker_client = create_docker_client(
                ip=nodes_config_dict['ips'][tainted_node], port=2376, logger=logger)

            docker_orchestrate(docker_client, logger=logger)

        else:
            raise UnsupportedOrchestratorException(
                tainted_node, nodes_config_dict['orchestrator'][tainted_node])

    return 'Taints and orchestration done'


    # Program execution
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=9999)
