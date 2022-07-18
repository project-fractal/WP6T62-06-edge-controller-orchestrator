import kubernetes
import docker
import docker.errors


class UnsupportedOrchestratorException(Exception):
    def __init__(self, hostname, orchestrator):
        self.hostname = hostname
        self.orchestrator = orchestrator
        self.message = f'The Orchestrator {orchestrator} for node {hostname} is not supported'
        super().__init__(self.message)


def taint_nodes(taints, hostname, resources, dict_info_json, logger):

    for resource in resources:

        # Check CPU is not over 80%
        if resource == 'cpu':

            if dict_info_json[resource]['total'] > 80:

                CPU_OK = False

                logger.warning(
                    f'CPU in node {hostname} is over 80%: CPU = {dict_info_json[resource]["total"]}')

                # Check if node is already tainted
                if hostname in taints.keys():
                    logger.info(
                        f'Node {hostname} is already tainted as {taints[hostname]}')
                # If not tainted, taint the node
                else:
                    logger.info(
                        f'Tainting node {hostname} to avoid scheduling of any other containers')

                    taints[hostname] = 'NoSchedule'

        # Check if RAM memory is over 80%
        elif resource == 'mem':
            if dict_info_json[resource]['percent'] > 80:

                MEM_OK = False

                logger.warning(
                    f'Memory in node {hostname} is over 80%: MEM % = {dict_info_json[resource]["percent"]} %')

                # Check if node is already tainted
                if hostname in taints.keys():
                    logger.info(
                        f'Node {hostname} is already tainted as {taints[hostname]}')
                # If not tainted, taint the node
                else:
                    logger.info(
                        f'Tainting node {hostname} to avoid scheduling of any other containers')

                    taints[hostname] = 'NoSchedule'

        elif resource == 'load':
            if dict_info_json[resource]['min5'] > 0.8:

                LOAD_OK = False

                logger.warning(
                    f'Load average at 5min in node {hostname} is over 80%: Load(min5) % = {dict_info_json[resource]["min5"]} %')

                # Check if node is already tainted
                if hostname in taints.keys():
                    logger.info(
                        f'Node {hostname} is already tainted as {taints[hostname]}')
                # If not tainted, taint the node
                else:
                    logger.info(
                        f'Tainting node {hostname} to avoid scheduling of any other containers')

                    taints[hostname] = 'NoSchedule'

        new_taints = taints

        return new_taints


def create_docker_client(hostname, port):
    # Create the Docker client instance
    try:
        env = {'DOCKER_HOST': f'{hostname}:{port}'}
        docker_client = docker.client.from_env(environment=env)

        # Check the server responsiveness
        docker_client.ping()

        return docker_client

    except docker.errors.APIError as e:
        print(e)


def create_k8s_client():
    # TODO: Instantiate k8s client
    pass


def actions(hostname, orchestrator, resources, dict_info_json, taints, logger):

    # If all of these are True at the end, untaint the node if tainted.
    global CPU_OK
    global MEM_OK
    global LOAD_OK

    CPU_OK = True
    MEM_OK = True
    LOAD_OK = True

    new_taints = taint_nodes(
        taints, hostname, resources, dict_info_json, logger)

    # Untaint the node if everything is OK
    if CPU_OK and MEM_OK and LOAD_OK and hostname in taints.keys():
        taints.pop(hostname)

    # Take actions on K8S and Docker accordingly:
    if orchestrator == 'kubernetes':
        pass
        # TODO: Take actions for Kubernetes

    elif orchestrator == 'docker':

        client = create_docker_client(hostname, port=2376)

    else:
        raise UnsupportedOrchestratorException(hostname, orchestrator)

    return new_taints
