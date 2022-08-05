def check_previous_taints(new_taints, logger):

    try:
        with open(file='./taints.txt', mode='r') as already_tainted:

            # Read the list of previously tainted nodes
            already_tainted_nodes = already_tainted.readlines()

            # Remove the newline character
            for i in range(len(already_tainted_nodes)):
                already_tainted_nodes[i] = already_tainted_nodes[i].strip()

    except Exception as e:
        logger.warning('First time applying taints!')
        already_tainted_nodes = []

    with open(file='./taints.txt', mode='w') as already_tainted:
        new_tainted_nodes = []
        untainted_nodes = []

        for node in new_taints:
            if node in already_tainted_nodes:
                logger.info(f'{node} was previously tainted.')
            else:
                logger.info(
                    f'{node} not tainted previously, new tainted node.')
                new_tainted_nodes.append(node)

        for node in already_tainted_nodes:
            if node not in new_taints:
                logger.info(
                    f'{node} no longer tainted... Removing from tainted lists')
                already_tainted_nodes.remove(node)
                untainted_nodes.append(node)

        for i in range(len(already_tainted_nodes)):
            already_tainted.writelines(already_tainted_nodes[i] + '\n')

        for i in range(len(new_tainted_nodes)):
            already_tainted.writelines(new_tainted_nodes[i] + '\n')
    # At the end of the loop, return the list of previously tainted nodes and new tainted nodes to orchestrate.
    return already_tainted_nodes, new_tainted_nodes, untainted_nodes
