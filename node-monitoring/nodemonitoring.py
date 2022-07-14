import requests
import os 
import time
import json
from utils.infotreatment import info_treatment
from utils.logger import set_logger


# Set server constants
PROTOCOL = 'http://'
BASE_RESOURCE = '/api/3/'
RESOURCE_LIST = ['cpu', 'mem', 'alert', 'load', 'processlist']

logger = set_logger()

## Node Operations
def check_status(url):
    try:
        requests.get(url=url)
        return True

    except requests.exceptions.ConnectionError as e:
        logger.info("The connection was refused, is the node alive?")
        logger.error(e)
        return False

def get_info(url, node):
    
    json_resource_list = []

    for resource in RESOURCE_LIST:
        response = requests.get(url=url+BASE_RESOURCE+resource).content
        json_resource_list.append(response)
        logger.info(f'{node} resource {resource} info: ' + str(response))

    return json_resource_list




## Program execution
if __name__ == "__main__":
    
    # Open the nodes file and fill a list with the different nodes to monitor
    with open('./node-monitoring/nodes.txt', 'r') as nodes:
        nodelist = []
        for node in nodes.readlines():
            node = node.replace('\n','')
            nodelist.append(node)
            logger.info(f'Adding new node to monitor: {node}')

    down_nodes = []

    while True:

        for node in nodelist:
            
            URL=f'{PROTOCOL}{node}'

            # For down nodes, check if still down
            if node in down_nodes:
                # Update the list of down nodes
                if check_status(URL):
                    
                    logger.info(f'{node} is live again, getting node info')
                    down_nodes.remove(node)
                    
                    # Node is now live, get its information
                    try:
                        # node_info is an array of jsons
                        node_info = get_info(URL, node)

                        info_treatment(node_info, node, logger)

                    except requests.exceptions.ConnectionError as e:    
                        ALIVE = check_status(URL)
                        if not ALIVE:
                            logger.info(f'{node} server is down, reconnecting...')
                            down_nodes.append(node)

            # For alive nodes, get the node info
            else:
                try:
                    # node_info is an array of jsons
                    node_info = get_info(URL, node)

                    info_treatment(node_info, node, logger)

                except requests.exceptions.ConnectionError as e:    
                    ALIVE = check_status(URL)
                    if not ALIVE:
                        logger.info(f'{node} server is down, reconnecting...')
                        down_nodes.append(node)

        time.sleep(5)
