import requests
import time
import yaml
from utils.infotreatment import info_treatment
from utils.logger import set_logger
from utils.actions import UnsupportedOrchestratorException, actions
from utils.constants import RESOURCE_LIST, PROTOCOL, BASE_RESOURCE

logger = set_logger()


def load_config():
    # Starting configuration
    with open('./resource_manager/nodes.yaml', 'r') as configfile:
        try:
            logger.info('Reading configuration file nodes.yaml')
            nodeconfig = yaml.safe_load(configfile)

        except yaml.YAMLError as e:
            logger.error(f'Configuration file could not be read: {e}')
    return nodeconfig


# Below are the functions that perform node operations


def check_status(url, node):
    try:
        requests.get(url=url)
        return True

    except requests.exceptions.ConnectionError as e:
        logger.info(f'The connection was refused, is the node {node} alive?')
        logger.error(e)
        return False


def request_node_info(url, node, resources=RESOURCE_LIST):

    json_resource_list = []

    # Check if the YAML contains custom resources to monitor, else monitor all supported resources
    for resource in resources:
        response = requests.get(url=url+BASE_RESOURCE+resource).content
        json_resource_list.append(response)

    return json_resource_list


def process_info(URL, hostname, resources=RESOURCE_LIST):
    try:
        # node_info is an array of jsons
        node_info = request_node_info(URL, hostname, resources)

        # info_treatment() returns the node information in a list of resources in json format
        json_info_list = info_treatment(node_info, hostname, resources, logger)

        # The json list is mapped to its respective resources into a dict
        dict_json_info = {}

        for i in range(len(json_info_list)):
            dict_json_info[resources[i]] = json_info_list[i]

        return dict_json_info

    except requests.exceptions.ConnectionError as e:
        ALIVE = check_status(URL, hostname)
        if not ALIVE:
            logger.info(f'{hostname} server is down, reconnecting...')
            down_nodes.append(hostname)


# Program execution
if __name__ == '__main__':

    # Open the nodes file and fill a list with the different nodes to monitor
    logger.info('Opening configuration file nodes.yaml')

    # Process config file
    logger.info('Loading node configuration...')
    nodeconfig = load_config()

    # Parse YAML config into python objects
    hostnamelist = []
    node_endpoints = {}
    node_resources = {}
    node_orchestrators = {}

    for node in nodeconfig:
        # List of hostnames
        hostnamelist.append(node['node']['hostname'])

        # Endpoint of the node
        endpoint = str(node['node']['IP']) + ':' + str(node['node']['port'])

        # Dictionary {"hostname":"endpoint"}
        node_endpoints[node['node']['hostname']] = endpoint

        # Dictionary {"hostname":["resource1", "resource2", ...]}
        if 'resources' in node['node'].keys():
            node_resources[node['node']
                           ['hostname']] = node['node']['resources']

        # Dictionary {"hostname": "orchestrator"}
        if 'orchestrator' in node['node'].keys():
            node_orchestrators[node['node']['hostname']
                               ] = node['node']['orchestrator']

        logger.info(
            f'Node {node["node"]["hostname"]} configuration successfully loaded!')

    logger.info('All nodes successfully loaded!')

    # Empty list of down nodes to be updated later
    down_nodes = []

    # First check of the availability of the nodes
    for hostname in hostnamelist:
        logger.info(f'Checking availability status of node {hostname}...')
        ipport = node_endpoints[hostname]
        URL = f'{PROTOCOL}{ipport}'

        if check_status(URL, hostname):
            logger.info(f'Node {hostname} is live!')
        else:
            down_nodes.append(hostname)
            logger.info(f'Node {hostname} is down!')

    # Start the loop
    while True:

        for hostname in hostnamelist:

            ipport = node_endpoints[hostname]
            URL = f'{PROTOCOL}{ipport}'

            # For down nodes, check if still down
            if hostname in down_nodes:
                # Update the list of down nodes
                if check_status(URL, hostname):

                    logger.info(f'{hostname} is live again, getting node info')
                    down_nodes.remove(hostname)

                    # Node is now live, get its information
                    if node_resources[hostname] is None:
                        processed_info = process_info(URL, hostname)
                    else:
                        processed_info = process_info(
                            URL, hostname, node_resources[hostname])

            # For alive nodes, get the node info
            else:
                if hostname in node_resources.keys():
                    processed_info = process_info(
                        URL, hostname, node_resources[hostname])
                else:
                    processed_info = process_info(URL, hostname)

                # Take actions based on the gathered information
                # The actions() function is where the logic of alarms, actions to take and
                # custom orchestration is done.
                # While infotreatment.py only parses the information into easy-handling formats,
                # actions implements the logic on what decisions and actions to take based on the results.

                # processed_info is a dict: {resource: values}, e.g. {"cpu": {total: 1.9, ...}, "mem": {total: 8.1, ...}}
                try:

                    if hostname in node_resources.keys() and hostname in node_orchestrators.keys():

                        taken_actions = actions(
                            node=hostname, orchestrator=node_orchestrators[hostname], resources=node_resources[hostname], dict_info_json=processed_info)

                    elif hostname not in node_resources.keys():
                        taken_actions = actions(
                            node=hostname, orchestrator=node_orchestrators[hostname], resources=RESOURCE_LIST, dict_info_json=processed_info)
                    elif hostname not in node_orchestrators.keys():
                        # Nothing to do if node is not orchestrated
                        logger.info(
                            f'Node {hostname} is not being orchestrated.')
                        taken_actions = 'None'

                    logger.info('Taken actions: ' + str(taken_actions))

                except UnsupportedOrchestratorException as e:
                    logger.error(e)

        time.sleep(5)
