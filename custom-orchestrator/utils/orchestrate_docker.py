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


def orchestrate(client, logger):
    # TODO: Take actions for Docker

    # Limit the container resources from each of the containers in the host apart from Glances
    try:
        container_list = client.containers.list(all=True)

        logger.info(container_list)

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
