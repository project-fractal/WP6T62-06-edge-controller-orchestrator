""" 
This script contains the functions in charge of saving the initial status of the deployments in a K8s cluster,
so that it is possible to restore any given deployment to the original state after any modification in the replicanumber
has been made
"""


"""
This function saves the initial status of each deployment. Creates a csv file containing the name, namespace and the replica number
separated by ";" -> deploy_name ; namespace ; replica_number \n
"""
def save_initial_deployment_status(deployment_list, logger):
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


"""
This function reads the file where the deployment information has been saved
and returns the number of replicas of a given deployment name and its namespace
"""

def get_replica_num(name, namespace, logger):
    deployment_data = name + "; " + namespace + ";"

    with open("./deployments.txt", mode='r') as dplmnt_fp:
        lines = dplmnt_fp.lines()
        for line in lines:
            # return the corresponding number of replicas once found
            if line.find(deployment_data) != -1: 
                nReplicas = int(line.split("; ")[2][0]) 
                return nReplicas
        
