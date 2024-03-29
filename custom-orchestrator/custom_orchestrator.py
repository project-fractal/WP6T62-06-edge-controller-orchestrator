from ast import literal_eval

from flask import Flask, request

from utils.logger import set_logger
from utils.constants import API_BASE
from utils.check_taints import check_previous_taints
from utils.deployment_status import save_initial_deployment_status
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
        # TODO: check this -> all deployments are stored in a file when first executed
        # gets every deployment in every node -> how to control to which node a deployment belongs to?
#        k8s_client = create_k8s_client(logger)
        # Save initial status of the cluster for further replica number modification and restoring
        # initial_deployments = k8s_client.list_deployment_for_all_namespaces()
        # deployment_original_state = save_initial_deployment_status(initial_deployments, logger)
    # Keep awareness of Tainted nodes and when untainted, remove restrictions
    new_taints = request.json

    previously_tainted_nodes, new_tainted_nodes, untainted_nodes = check_previous_taints(
        new_taints, logger=logger)

    logger.info(
        'Orchestrating and aplying the following restrictions to nodes:\n')
    logger.info('Nodes previously tainted and still tainted: \n')
    for node in previously_tainted_nodes:
        logger.info(node)

    logger.info('New tainted nodes: \n')
    for node in new_tainted_nodes:
        logger.info(node)

    logger.info('Nodes untainted: \n')
    for node in untainted_nodes:
        logger.info(node)

    # Take actions on K8S and Docker accordingly:

    for tainted_node in new_tainted_nodes:
        logger.info(tainted_node +
                    ' is tainted for the first time. Applying custom orchestration...')

        if nodes_config_dict['orchestrator'][tainted_node] == 'kubernetes':
            # TODO: Take actions for Kubernetes
            k8s_client = create_k8s_client(
                nodes_config_dict['ips'][tainted_node])

            k8s_orchestrate(
                k8s_client, tainted_node, previously_tainted=False, untainted=False, logger=logger)

        elif nodes_config_dict['orchestrator'][tainted_node] == 'docker':
            docker_client = create_docker_client(
                ip=nodes_config_dict['ips'][tainted_node], port=2376, logger=logger)

            docker_orchestrate(
                docker_client, previously_tainted=False, untainted=False, logger=logger)

        else:

            raise UnsupportedOrchestratorException(
                tainted_node, nodes_config_dict['orchestrator'][tainted_node])

    for tainted_node in previously_tainted_nodes:
        logger.info(tainted_node +
                    ' was previously tainted. Applying more restrictive custom orchestration...')

        if nodes_config_dict['orchestrator'][tainted_node] == 'kubernetes':
            # TODO: Take actions for Kubernetes
            k8s_client = create_k8s_client(
                nodes_config_dict['ips'][tainted_node])

            k8s_orchestrate(k8s_client, tainted_node, previously_tainted=True,
                            untainted=False, logger=logger)

        elif nodes_config_dict['orchestrator'][tainted_node] == 'docker':
            docker_client = create_docker_client(
                ip=nodes_config_dict['ips'][tainted_node], port=2376, logger=logger)

            docker_orchestrate(
                docker_client, previously_tainted=True, untainted=False, logger=logger)

        else:
            raise UnsupportedOrchestratorException(
                tainted_node, nodes_config_dict['orchestrator'][tainted_node])

    for untainted_node in untainted_nodes:
        logger.info(
            f'{untainted_node} is now untainted. Lifting restrictions on the node...')

        if nodes_config_dict['orchestrator'][untainted_node] == 'kubernetes':
            # TODO: Take actions for Kubernetes
            k8s_client = create_k8s_client(
                nodes_config_dict['ips'][untainted_node])

            k8s_orchestrate(k8s_client, untainted_node, previously_tainted=False,
                            untainted=True, logger=logger)

        elif nodes_config_dict['orchestrator'][untainted_node] == 'docker':
            docker_client = create_docker_client(
                ip=nodes_config_dict['ips'][untainted_node], port=2376, logger=logger)

            docker_orchestrate(
                docker_client, previously_tainted=False, untainted=True, logger=logger)

    return 'Taints and orchestration done'


    # Program execution
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=9999)
