# T6.2 - Edge Controller & Custom Edge Ochrestrator
<!-- TODO Adecuar a docu fractal -->
This project contains necessary files to build the tools to perform node monitoring and resource managing tasks within a cluster. 

## Edge Controller

The main modules of this tool are the metrics-exporter and the resource-manager:

On the one hand, the **resource-manager** is deployed in the nodes designed as master, which are in charge of controlling and monitoring the other nodes. This module can be deployed on both edge servers and edge nodes as the functionality remains the same.

The main functionalities of this module are collecting information of the nodes to monitor, found in the `nodes.yaml`, and take actions based on some user defined rules when executing the `Kubernetes` or `Docker` orchestrators.

On the other hand, the **metrics-exporter** is deployed in each of the nodes included in the node monitoring list within `nodes.yaml` file, and creates a container running a `Glances` instance. This tool, similar to utilities such as `top`, collects both metrics and system status information (CPU status or used percentage, memory usage, etc.) and exposes that information in the port 61208 through a REST API. The information is collected every 5 seconds, and if any node were to fail, `Glances` still collects and retains the corresponding data just in case the node is restored. 

The collected information is sent to the custom edge orchestrator and used to decide whether a node is considered as tainted or not depending on the values collected and if they are above some fixed thresholds, making it possible to avoid deployments on a given node if the resources are scarce.

## Custom Edge Orchestrator

The custom edge orchestrator is used to manage the resources of the nodes listed in `nodes.yaml`, and it is designed to modify and take actions on both `Kubernetes` and `Docker` nodes, as well as user defined orchestrators. 

This module ingests the information from the metrics-exporter and uses it to restrict or free the resources of each node depending on the values of the system metrics collected. These monitoring actions to be taken have two different levels of restriction, depending on whether the node has already had its resources limited:

* If it is the first time that the node is running out of resources, the resources are mildly limited, and new deployments are still allowed
* If the node has already had resource limitation actions applied, it is marked as tained and new deployments are forbidden until the node is marked as available again

These actions have different consecuences depending on the orchestrator. For example, in Docker environments, the containers within the node are stopped when resources have been restricted and restarted when node resources are available again; in the case of Kubernetes, as the containers cannot be stopped, the replica numbers of the deployments are modified.