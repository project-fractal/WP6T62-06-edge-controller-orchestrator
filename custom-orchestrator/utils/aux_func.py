# auxiliary functions to set nodes as tainted or untainted

# taint/untaint nodes using the patch_node function
# source: https://stackoverflow.com/questions/68174233/how-to-delete-a-node-taint-using-pythons-kubernetes-library
def taint_node(kube_client, node_name):
    taint_patch = {"spec": {"taints": [{"effect": "NoSchedule", "key": "test", "value": "True"}]}}
    return kube_client.patch_node(node_name, taint_patch)

def untaint_node(kube_client, node_name):
    remove_taint_patch = {"spec": {"taints": []}}
    return kube_client.patch_node(node_name, remove_taint_patch)

# scale replicas in a deployment
def scale_replicas(client, name, ns, replicaNumber):
    patch_body = {"spec": {"replicas": replicaNumber}}
    client.patch_namespaced_deployment_scale(name, ns, patch_body)
