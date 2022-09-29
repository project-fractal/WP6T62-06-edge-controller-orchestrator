# WP6T602-06 Orchestrator
This project contains all the code and documentation about the Edge Controller component for Fractal, which is a custom Orchestrator that can be deployed on noth High-End and Mid-End Fractal Edge Nodes to orchestrate the overall system and provide context awareness to each of the Fractal Nodes and the overall system.

### How does the component satisfy the WP/FRACTAL objectives?

WP6T62-06 Orchestration component provides a set of tools to be implemented in the Fractal Edge Node. This set of tools is in charge of monitoring the overall status and monitoring the resources of the Fractal Edge nodes both individually and collectively. This component addresses the following WP6 objectives (in bold):

- Analysis of existing open-source edge and cloud platforms implementations in order to determine a potential FRACTAL reference engineering framework. It will consist of: (i) an edge processing platform and (ii) **an edge controller infrastructure**.

- **Design and implementation of the FRACTAL software processing framework based on microservices for the integration of processing capacities** (AI and safe autonomous decision algorithms developed in WP5) and enabling the connection of IoT devices using standard or proprietary protocols over Ethernet and cellular networks.

- **Edge platform orchestration, monitoring the physical and application integrity at edge locations with the ability to autonomously enable corrective actions when necessary**.

- Specification of a generic data model and common interface to communicate with the cloud.

- **Design and implementation of the FRACTAL edge node controller infrastructure (in the cloud) for the management and update of the edge processing platform**.

- **Adaptation of the FRACTAL software components to allow a fractal growth (scalability) from low to the high computing edge node**.

- Test and validation of the FRACTAL engineering framework by means of simulations and preliminary laboratory trials (TRL4).

- Integration, test and validation of the FRACTAL wireless communications nodes (4G/5G, NB-IoT/LTE-M, as stand-alone subsystem (TRL6).

As it can be seen in the fulfilled objectives, this component is of great importance when demonstrating the orchestrating and scaling capabilities of the Fractal Edge architecture.

## Getting Started

### Prerequisites

This component is mostly Python code and containers running, so it does not have heavy requirements. However, make sure that the following prerequisites are fulfilled:

* Python3.8 or later
* Docker Engine (latest)
* Kubernetes (Tested for v1.24.0 and later)

This project contains all the necessary files to build the tools to perform node monitoring and resource managing tasks within a cluster, no other code or external files are required.

### Edge controller

The Edge Controller is also composed of two main modules, the metrics exporter and the resource manager.

The Edge Controller is in charge of collecting all the resources information inside each of the Fractal nodes.

- The **resource-manager** is deployed in the master nodes, which are in charge of controlling and monitoring the rest of the cluster (including themselves). This module can be deployed on both edge servers and edge nodes and the functionality remains the same.

- The **metrics-exporter** is deployed in each of the nodes included in the node monitoring list within `nodes.yaml` file, and creates a container running a `Glances` instance. This tool, similar to utilities such as `top`, collects both metrics and system status information (CPU status or used percentage, memory usage, etc.) and exposes that information in the port 61208 through a REST API. The information is collected every 5 seconds, and if any node eventually fails, `Glances` still collects and retains the corresponding data. If the node is restored, then it will be monitored accordingly again.

The collected information is sent to the custom edge orchestrator and used to decide whether a node is considered as tainted (low on resources and restricted) or not, depending on the available resources. If any of the monitored resources are above some fixed thresholds, that node is no longer able to perform any new container deployments until the resource limitation is lifted.

### Custom Edge Orchestrator

The custom edge orchestrator is used to manage the resources of the nodes listed in `nodes.yaml`, and it is designed to modify and take actions on both `Kubernetes` and `Docker` nodes, as well as user defined orchestrators.

This module ingests the information from the metrics-exporter and uses it to restrict or free the resources of each node depending on the values of the system metrics collected. These monitoring actions to be taken have two different levels of restriction, depending on whether the node has already had its resources limited:

* The first time the node is running out of resources, the resources are mildly limited, and new deployments are still allowed

* The node has already had resource limitation actions applied, it is marked as tained and new deployments are forbidden until the node is tagged as available again.

These actions have different consecuences depending on the orchestrator. For example, in Docker environments, the containers within the node are sequentially stopped when resources have been restricted and restarted when node resources are available again; in the case of Kubernetes, the number of replicas for each deployments are down-scaled until the restrictions are lifted. This way the Edge Orchestrator always makes sure that the nodes are not exhausted on resources by balancing the container pressure.

## Installation // Build

Following a highly-decoupled microservices approach, there are two main software components inside this tool, the Edge Controller and the Custom Edge Orchestrator.

Below a tutorial is provided to build and the necessary containers for each of the tool's components:

### Edge controller

The Edge controller has two main containers, the **metrics-exporter** and the **resource-manager**:

#### metrics-exporter

Before building the Docker container image with the `glances` monitoring service, make sure to configure the glances monitoring with your own alerts, login and metrics preferences in the `/metrics-exporter/glances.conf` file. The default configuration file will be used otherwise.

To build the metrics-exporter container image, execute the following command:

```
docker build -t metrics-exporter metrics-exporter
```

Then to run the metrics-exporter container on each of the nodes to be monitored, execute the `run.sh` script in the metrics-exporter directory:

```
./metrics-exporter/run.sh
```
It is important to run the container with the configuration in the run.sh script, because the `glances` instance running on the container will not be able to monitor the host resources if it not running in the host network (specified in the --network=host flag.

#### resource-manager

Once the metrics-exporter container is running on each of the Fractal Edge nodes to monitor, we must provide the hosts' information to the resource manager before executing it. This is done through the `nodes.yaml` file where the hostname, IP, port (61208 by default), orchestrator being used (docker or kubernetes) and the desired resources to monitor (leave this field blank to monitor ALL available resources, which is the preferred option).

You must also provide information about the host that will be running the custom-orchestrator, only hostname, IP and port (9999 by default) are required.

You can find a sample nodes.yaml file in the `/resource-manager/nodes.yaml` file, where the commented lines are the optional features.

Once the `nodes.yaml` file is complete, build the Docker container image by running:

```
docker build -t resource-manager resource-manager
```

And run it with the provided `run.sh` script:

```
./resource-manager/run.sh
```

You will probably need to restart this container until the configuration is matched with your nodes, so a restart script is also provided for simplicity:

```
./resource-manager/restart.sh
```

You can now access the **resource-manager** container logs with `docker logs <resource-manager>` (check the container's name) and make sure the resource manager is correctly monitoring the Fractal Edge nodes specified in the nodes.yaml file.

With this two containers running (the **resource-manager** on the master node, and the **metrics-exporter** running on every node) you already have the basic functionality of resource monitoring on each of the nodes, and if any of the nodes is exhausted, you will get an updated listo f tainted nodes in the resource-manager container logs. Now we are ready to build the **custom-orchestrator** container and deploy the whole orchestration capabilities into our Fractal Edge Platform.

### Custom Orchestrator

The last container to be built is the **custom-orchestrator**. This container should be deployed on the master node, or at least the node that is going to perform the orchestration operations, this is, a node which can reach all the other nodes' Docker daemons (which should be previously exposed), or the Kubectl API.

To build this container image, run:

```
docker build -t custom-orchestrator custom-orchestrator
```

And run this container with the provided `run.sh` script:

```
./custom-orchestrator/run.sh
```

Once deployed, this container exposes a REST API which will be reached by the resource-manager, providing the information given in the `resource-manager/nodes.yaml` file. Confirm that this information has been received by checking the **custom-orchestrator** container logs.


## Usage

Once the container images have been created and the functioning of the independent containers has been checked, they must be deployed into the nodes in a specific order.

### Deployment

#### #1 metrics-exporter

First, the **metrics-exporter** container must be deployed on each of the nodes to be monitored, either master or worker nodes, by running the above described `run.sh` script. To check that the container is working properly, you can go to `http://<NODE_IP>:61208` or execute the command:

```
curl http://<NODE_IP>:61208/api/3/cpu
```

which should display the cpu usage information of your node.

#### #2 custom-orchestrators

Deploy the **custom-orchestrator** container on the node you plan to be the custom orchestrator. This node should have access and enough permissions to perform kubectl operations in case it is a kubernetes environment, or send requests to the Docker daemons of the rest of the hosts (which should be exposed following this guidelines: [Docker Daemon](https://docs.docker.com/config/daemon/))

#### #3 resource-manager

Fill in the information in the `nodes.yaml` file before starting up this container. This information will be used by the resource-manager and the custom-orchestrator to be able to communicate with the nodes and send the orchestration and resource managing communications.

Deploy the **resource-manager** container on the node which is going to perform the orchestration strategies (not required to be the same node as the custom-orchestrator).

Once all the containers have been deployed, the resource-manager and the custom-orchestator containers logs can be accessed to check that the resource-manager has successfully connected to each of the managed nodes and also recognized the orchestrating node as the custom-orchestrator.


### Stress a node

These orchestration mechanisms and resource management happen on the background, so in systems which are working normally, nothing should happen.

You can try stressing your nodes to increase the CPU usage while monitoring the **resource-manager** logs to see what operations are happening into the node. This will work better if the stressed node is part of a K8S cluster or has its Docker daemon exposed with several containers running.

We recommend to use the `yes` command in the node to be stressed, but be careful to cancel this operation once you have checked that the resource manager and the orchestration is being executed as expected.

## Additional Documentation and Acknowledgments

* Developed by ZYLK
