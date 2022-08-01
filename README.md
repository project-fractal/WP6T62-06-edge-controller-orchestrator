# T6.2 - Edge Controller & Custom Edge Orchestrator

## Edge Controller
En este proyecto hay dos directorios, edge-monitoring y node-monitoring.

**resource-manager** se despliega en los nodos que actúen como controladores del resto (nodos master, o nodos dedicados a monitorizar). Se puede desplegar en un servidor Edge, o en cualquiera de los propios nodos Edge, la funcionalidad es la misma.

Tiene dos funciones principales:

* Recopilar la información sobre todos los nodos de la lista en `nodes.yaml`.
* Tomar acciones en base a unas reglas sobre los orquestadores `kubernetes` o `docker`.


**metrics-exporter** se despliega en cada uno de los nodos Edge que se incluirán en la lista de nodos a monitorizar `nodes.yaml`, y se encarga de levantar un contenedor con una instancia de `glances`, una herramienta similar a `top` que recopilar métricas e información sobre el estado de la CPU, la memoria etc y las expone en el puerto 61208 como una API REST.


La información de cada nodo se recopila cada 5 segundos. Si alguno de los nodos se cae, el programa sigue teniéndolo en cuenta por si vuelve a estar online. Se expone información por consola como el % de CPU consumido, memoria RAM disponible y carga del procesador.

Tras el procesado de la información recibida de glances, se toman una serie de acciones:
* Comprobar si alguno de los parámetros de CPU, RAM, o carga del procesador superan unos valores umbral arbitrarios. Los nodos pasan entonces a estar tainteados, con una etiqueta NoSchedule.

Esta información será enviada al Custom Edge Orchestrator para que impida el despliegue o creación de nuevos contenedores o tareas sobre esos nodos, ya sea a través del demonio de Docker expuesto o de la API de K8S.

## Custom Edge Orchestrator

### To be done
