from http import client
import docker
from docker.errors import APIError


def create_client(ip, port, logger):
    # Create the Docker client instance
    try:
        env = {'DOCKER_HOST': f'{ip}:{port}'}
        docker_client = docker.client.from_env(environment=env)

        # Check the server responsiveness
        docker_client.ping()

        return docker_client

    except APIError as e:
        logger.error(e)


def orchestrate(client, previously_tainted: bool, untainted: bool, logger):

    # Get the list of containers
    try:
        container_list = client.containers.list(all=True)

        logger.info(container_list)
    except APIError as e:
        logger.error('Error while orchestrating Docker host: ' + e)

    # Check if the node is untainted and remove restrictions
    if untainted:
        # Restart all stopped containers
        try:
            for cont in container_list:
                if cont.attrs['State']['Status'] == 'exited':
                    logger.info(f'Restarting exited container: {cont}')
                    cont.start()

                elif cont.attrs['State']['Status'] == 'running':
                    pass

                else:
                    pass

            return
        except APIError as e:
            logger.error('Error while orchestrating Docker host: ' + e)

    # Check if the node was already tainted
    if previously_tainted:
        # If it was previously tainted, stop containters one by one
        try:
            for cont in container_list:
                # Check if it is glances container
                logger.info(cont)

                if 'glances' in str(cont.attrs['Args']):
                    logger.warning(
                        'Avoiding limiting resources of the glances container')
                    pass
                else:
                    cont.stop()
                    break

        except APIError as e:
            logger.error('Error while orchestrating Docker host:' + e)

    else:
        # If it's the first time the node gets tainted
        # Limit the container resources from each of the containers in the host apart from Glances
        try:
            for cont in container_list:
                logger.info(cont)

                if 'glances' in str(cont.attrs['Args']):
                    logger.warning(
                        'Avoiding limiting resources of the glances container')
                    pass
                else:

                    logger.warning('Limiting resources of container ' +
                                   str(cont.attrs['Name']))

                    limited_container = client.containers.get(
                        str(cont.attrs['Id']))
                    limited_container.update(
                        mem_limit='1g', memswap_limit='1g', cpu_period=100000, cpu_quota=50000)

                    logger.info('Container ' +
                                str(cont.attrs["Name"]) + ' has had its resources limited')
        except APIError as e:
            logger.error('Error while orchestrating Docker host: ' + e)
            return

    return
