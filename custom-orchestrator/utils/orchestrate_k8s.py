from kubernetes import config, client as kclient
from kubernetes.client.exceptions import ApiException
from utils.aux_func import taint_node, untaint_node, scale_replicas, limit_node_resources, remove_node_resource_limitations
from utils.deployment_status import save_initial_deployment_status, get_replica_num


"""
This function creates the k8s client needed to retrieve and modify k8s cluster resource information
It is intended to be executed from a pod, therefore there are some settings that must be defined beforehand.
More details can be found in "permissions.yaml".
Returns the client object from kubernetes library after loading the cluster configuration
With this client, it is possible to summon the needed functions from classes CoreV1Api and AppsV1Api
"""
def create_client(logger):
    try:
        # load the cluster configuration
        config.load_incluster_config()

        # save initial deployment status
        save_initial_deployment_status()

        # return kclient object
        return kclient
    except kclient.exceptions.ApiException as e:
        logger.error(e)
    return


"""
Main function to orchestrate a K8s cluster. After obtaining the current deployments,
starts to check whether a node needs to be tainted, untainted or has been previously tainted 
in order to apply changes in the cluster to solve those situations. 
Takes the kclient object, a given node and its status (tainted, untainted) as input parameters 

The changes applied depend on the status of the node:
* If the node is flagged as untainted -> untaint that node and restore the deployments
* If the node is flagged as tainted -> mark as tainted and limit the resources
* If the node is flagged as previously tainted -> scale down the deployments within the node
"""
def orchestrate(client, node, previously_tainted: bool, untainted: bool, logger):
    try:
        # get current deployments
        dplmnt_list = client.AppsV1Api.list_deployment_for_all_namespaces()
        
        logger.info(dplmnt_list)
    except ApiException as e:
        logger.error(e)

    if untainted:
        try:
            # first, set the node as untainted
            logger.info(f"Untainting node {node}")
            untaint_node(client, node)
            for deploy in dplmnt_list.items:
                # check if any replica has to be restored
                n_replicas = deploy.to_dict().get("status").get("replicas")
                if n_replicas == None:
                    # get deployment data
                    name = deploy.to_dict().get("metadata").get("name")
                    ns = deploy.to_dict().get("metadata").get("namespace")
                    # remove resource limitations
                    logger.info("Removing namespace resource limitations")
                    remove_node_resource_limitations(client, ns)
                    logger.info(f"Restoring deployment: {name} in namespace {ns}")
                    nReplicas = get_replica_num(name, ns)
                    scale_replicas(client, name, ns, nReplicas)

        except ApiException as e:
            logger.error(e)

    if previously_tainted: # node has already been tainted -> resources have been limited -> scale down deployments

        for deploy in dplmnt_list.items:
            name = deploy.to_dict().get("metadata").get("name")
            if 'glances' in name:
                logger.warning("Avoiding limiting resources of the glances deployment")
            else:
                ns = deploy.to_dict().get("metadata").get("namespace")
                logger.info(f"Scaling down deployment: {name} in namespace {ns}")
                body_rep = {"spec": {"replicas": 0}}
                # decrease number of replicas to 0
                scale_replicas(client, name, ns, 0)
    else:
        # set node as tainted to avoid creating more deployments
        taint_node(client, node)
        # limit the resources for each namespace
        restricted_ns = []  # list to track which namespaces have limited resources
        for deploy in dplmnt_list.items:
            ns = deploy.to_dict().get("metadata").get("namespace")
            if ns not in restricted_ns: # check if resources of ns have already been limited -> may be unnecessary
                limit_node_resources(client, ns)
                restricted_ns.append(ns)


    return
