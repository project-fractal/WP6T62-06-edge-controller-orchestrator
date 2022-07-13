edge-monitoring se ejecuta desde los nodos Edge y levanta un contenedor con una instancia de Glances en el puerto 61208 al que se le pueden hacer queries.

node-monitoring se ejecuta desde un nodo que monitorice al resto (o a sí mismo), y se le pasa la lista de nodos desde el fichero nodos.txt.

Se ejecuta un script de Python que cada 5 segundos hace poll de la información expuesta en glances de cada uno de los nodos de la lista, de momento solo hace eso pero en el futuro se añadirá lógica para que esta información se procese y tomar decisiones.
