import requests
import os 
import logging
import time
        
# create logger
logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# add ch to logger
logger.addHandler(ch)

# Set server constants
PROTOCOL = 'http://'


## Node Operations
def check_status(url):
    try:
        requests.get(url=url)
        return True

    except requests.exceptions.ConnectionError as e:
        logger.info("The connection was refused, is the node alive?")
        logger.error(e)
        return False

def get_info(url):
    RESOURCE = "/api/3/cpu"
    
    response = requests.get(url=url+RESOURCE).content
    
    logger.info(response)

    return response

## Program execution
if __name__ == "__main__":
    
    # Open the nodes file and fill a list with the different nodes to monitor
    with open('./nodes.txt', 'r') as nodes:
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
                    try:
                        get_info(URL)
                        #TODO: Treat JSON info somehow
                    
                    except requests.exceptions.ConnectionError as e:    
                        ALIVE = check_status(URL)
                        if not ALIVE:
                            logger.info(f'{node} server is down, reconnecting...')
                            down_nodes.append(node)


            # For alive nodes, get the node info
            else:
                try:
                    get_info(URL)
                    #TODO: Treat JSON info somehow
                
                except requests.exceptions.ConnectionError as e:    
                    ALIVE = check_status(URL)
                    if not ALIVE:
                        logger.info(f'{node} server is down, reconnecting...')
                        down_nodes.append(node)

        time.sleep(5)
