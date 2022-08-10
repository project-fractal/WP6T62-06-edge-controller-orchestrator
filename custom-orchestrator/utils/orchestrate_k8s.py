from kubernetes import config, client as kclient
from kubernetes.client.exceptions import ApiException
from aux_func import taint_node, untaint_node, scale_replicas

# TODO: check that this function works
def create_client(logger):
    try:
        # load the cluster configuration
        config.load_incluster_config() # may change to use apikey config
        # k8s_client = kclient.CoreV1Api()
        k8s_apps = kclient.AppsV1Api()
        return k8s_apps
    except kclient.exceptions.ApiException as e:
        logger.error(e)
    return


"""
TODO:
# 1. find desiredReplicas for each deployment to restore all of the replicas once the node is untainted
# 1.1 the desired replicas parameter can be obtained through the replicaset itself:
# --> how to find the corresponding replicaset for each deployment through the client?
# 2. limit node/pod/deployment?? resources before tainting it
#
"""
def orchestrate(client, node, previously_tainted: bool, untainted: bool, logger):
    try:
        # get current deployments
        dplmnt_list = client.list_deployment_for_all_namespaces()
        logger.info(dplmnt_list)
    except ApiException as e:
        logger.error(e)

    if untainted:
        try:
            # first, set the node as untainted
            untaint_node(client, node)
            for deploy in dplmnt_list.items:
                # check if any replica has to be restored
                n_replicas = deploy.to_dict().get("status").get("replicas")
                if n_replicas == None:
                    # get deployment data
                    name = deploy.to_dict().get("metadata").get("name")
                    ns = deploy.to_dict().get("metadata").get("namespace")
                    logger.info(f"Restoring deployment: {name} in namespace {ns}")
                    scale_replicas(client, name, ns, 1) # TODO: get desired replicas
                # else:
                #     pass
        except ApiException as e:
            logger.error(e)

    if previously_tainted:
        # relanzar deployments con etiquetas nuevas
        for deploy in dplmnt_list.items:
            name = deploy.to_dict().get("metadata").get("name")
            if 'glances' in name:
                logger.warning("Avoiding limiting resources of the glances deployment")
            else:
                ns = deploy.to_dict().get("metadata").get("namespace")
                logger.info(f"Scaling down deployment: {name} in namespace {ns}")
                body_rep = {"spec": {"replicas": 0}}
                # TODO: decrease number of replicas by one or set directly to 0?
                scale_replicas(client, name, ns, 0)
    else:
        # set node as tainted to avoid creating more deployments
        # TODO: research pod/namespace/deployment/node resource limitations in kubernetes
        taint_node(client, node)

    return
