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
        # add header for later reading
        deployments.write("name; namespace; replicas\n")
        for dep in dep.to_dict().items:
            dep_name = dep.to_dict().get("metadata").get("name")
            dep_ns = dep.to_dict().get("metadata").get("namespace")
            dep_replicas = dep.to_dict().get("status").get("replicas")
            dep_detail = dep_name + "; " + dep_ns + "; " + str(dep_replicas) + "\n"
            deployments.write(dep_detail)
            deployed.append(dep_detail)

    logger.info("Deployment status saved")


# function to retrieve number of replicas of known deployment given name and namespace

def get_replica_num(name, namespace, logger):
    deployment_data = name + "; " + namespace + ";"

    with open("./deployments.txt", mode='r') as dplmnt_fp:
        lines = dplmnt_fp.lines()
        for line in lines:
            # return the corresponding number of replicas once found
            if line.find(deployment_data) != -1: 
                nReplicas = int(line.split("; ")[2][0]) 
                return nReplicas
        
