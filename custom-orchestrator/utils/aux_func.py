# import kubernetes.client as kclient
# auxiliary functions to set nodes as tainted or untainted

# taint/untaint nodes using the patch_node function
# source: https://stackoverflow.com/questions/68174233/how-to-delete-a-node-taint-using-pythons-kubernetes-library
def taint_node(kube_client, node_name):
    taint_patch = {"spec": {"taints": [{"effect": "NoSchedule", "key": "tainted", "value": "True"}]}}
    return kube_client.CoreV1Api().patch_node(node_name, taint_patch)

def untaint_node(kube_client, node_name):
    remove_taint_patch = {"spec": {"taints": []}}
    return kube_client.CoreV1Api().patch_node(node_name, remove_taint_patch)

# scale replicas in a deployment
def scale_replicas(client, name, ns, replicaNumber):
    patch_body = {"spec": {"replicas": replicaNumber}}
    client.AppsV1Api().patch_namespaced_deployment_scale(name, ns, patch_body)


# functions to add/remove resource quotas in a namespace

def limit_node_resources(client, deployment_ns):
    resource_quota = client.V1ResourceQuota(
        spec=client.V1ResourceQuotaSpec(
            hard={"limits.cpu": "700m", "limits.memory": "500M"}))
    resource_quota.metadata = client.V1ObjectMeta(namespace=deployment_ns, name=f"quota-{deployment_ns}")
    client.CoreV1Api().create_namespaced_resource_quota(deployment_ns, body=resource_quota)

def remove_node_resource_limitations(client, deployment_ns):
    client.CoreV1Api().delete_namespaced_resource_quota(name=f"quota-{deployment_ns}", namespace=deployment_ns)
