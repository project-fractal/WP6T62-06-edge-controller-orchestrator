import requests
import os
import time
import yaml
from utils.infotreatment import info_treatment
from utils.logger import set_logger
from utils.actions import actions
from utils.constants import RESOURCE_LIST, PROTOCOL, BASE_RESOURCE

logger = set_logger()


def load_config():
    # Starting configuration
    with open('./node-monitoring/nodes.yaml', 'r') as configfile:
        try:
            logger.info('Reading configuration file nodes.yaml')
            nodeconfig = yaml.safe_load(configfile)

        except yaml.YAMLError as e:
            logger.error(f'Configuration file could not be read: {e}')
    return nodeconfig


# Node Operations


def check_status(url, node):
    try:
        requests.get(url=url)
        return True

    except requests.exceptions.ConnectionError as e:
        logger.info(f'The connection was refused, is the node {node} alive?')
        logger.error(e)
        return False


def request_node_info(url, node):

    json_resource_list = []

    for resource in RESOURCE_LIST:
        response = requests.get(url=url+BASE_RESOURCE+resource).content
        json_resource_list.append(response)
        logger.info(f'{node} resource {resource} info: ' + str(response))

    return json_resource_list


def process_info(URL, hostname):

    try:
        # node_info is an array of jsons
        node_info = request_node_info(URL, hostname)

        actions(info_treatment(node_info, hostname, logger))

    except requests.exceptions.ConnectionError as e:
        ALIVE = check_status(URL, hostname)
        if not ALIVE:
            logger.info(f'{hostname} server is down, reconnecting...')
            down_nodes.append(hostname)


# Program execution
if __name__ == "__main__":

    # Open the nodes file and fill a list with the different nodes to monitor
    logger.info('Opening configuration file nodes.yaml')

    # Process config file
    logger.info('Loading node configuration...')
    nodeconfig = load_config()

    # Parse YAML config into python objects
    hostnamelist = []
    node_endpoints = {}

    for node in nodeconfig:
        # List of hostnames
        hostnamelist.append(node["node"]["hostname"])

        # Endpoint of the node
        endpoint = str(node["node"]["IP"]) + ":" + str(node["node"]["port"])

        # Dictionary {"hostname":"endpoint"}
        node_endpoints[node["node"]["hostname"]] = endpoint

        logger.info(
            f'Node {node["node"]["hostname"]} configuration successfully loaded!')

    logger.info('All nodes successfully loaded!')

    # Empty list of down nodes to be updated later
    down_nodes = []

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
                    process_info(URL, hostname)

            # For alive nodes, get the node info
            else:
                process_info(URL, hostname)

        time.sleep(5)
