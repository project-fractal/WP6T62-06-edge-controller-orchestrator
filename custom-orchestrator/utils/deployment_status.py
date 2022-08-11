import kubernetes

def save_initial_deployment_status(deployment_list, logger):
    # this script intends to save the initial state of every deployment
    # made in the kubernetes cluster, so that when the orchestrator decides to
    # scale or modify the deployment, it is possible to restore it to its original
    # state once the resources have been freed

    # check if file exists
    try:
        with open(file="./deployments.txt", mode='r') as deployments:
            deployed = deployments.readlines()
            for i in range(len(deployed)):
                deployed[i] = deployed[i].strip()
    except Exception as e:
        logger.warning("No deployments were made yet!")
        deployed = []


    with open(file="./deployments.txt", mode='w') as deployments:
        for dep in deployment_list.items:
            dep_name = deployment_list.get("metadata").get("name")
            dep_ns = deployment_list.get("metadata").get("namespace")
            dep_replicas = deployment_list.get("status").get("replicas")
            dep_detail = dep_name + "; " + dep_ns + "; " + dep_replicas + "\n"
            deployments.write(dep_detail)
            deployed.append(dep_detail)

    return deployed