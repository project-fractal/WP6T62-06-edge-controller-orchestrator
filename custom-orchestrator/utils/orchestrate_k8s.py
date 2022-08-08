from kubernetes import config, client as kclient
def create_client(logger):
    # client created to be executed inside a pod within the cluster
    try:
        # load the cluster configuration
        config.load_incluster_config()
        k8s_client = kclient.CoreV1Api()
        return k8s_client
    except kclient.exceptions.ApiException as e:
        logger.error(e)
    return


def orchestrate(client, previously_tainted: bool, untainted: bool, logger):

    return
