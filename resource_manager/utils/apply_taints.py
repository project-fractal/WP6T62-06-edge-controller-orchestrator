def taint_nodes(taints, hostname, resources, dict_info_json, logger):

    # If all of these are True at the end, untaint the node if tainted.
    CPU_OK = True
    MEM_OK = True
    LOAD_OK = True

    for resource in resources:

        # Check CPU is not over 80%
        if resource == 'cpu':

            if dict_info_json[resource]['total'] > 80:

                CPU_OK = False

                logger.warning(
                    f'CPU in node {hostname} is over 80%: CPU = {dict_info_json[resource]["total"]}')

                # Check if node is already tainted
                if hostname in taints.keys():
                    logger.info(
                        f'Node {hostname} is already tainted as {taints[hostname]}')
                # If not tainted, taint the node
                else:
                    logger.info(
                        f'Tainting node {hostname} to avoid scheduling of any other containers')

                    taints[hostname] = 'NoSchedule'

        # Check if RAM memory is over 80%
        elif resource == 'mem':
            if dict_info_json[resource]['percent'] > 80:

                MEM_OK = False

                logger.warning(
                    f'Memory in node {hostname} is over 80%: MEM % = {dict_info_json[resource]["percent"]} %')

                # Check if node is already tainted
                if hostname in taints.keys():
                    logger.info(
                        f'Node {hostname} is already tainted as {taints[hostname]}')
                # If not tainted, taint the node
                else:
                    logger.info(
                        f'Tainting node {hostname} to avoid scheduling of any other containers')

                    taints[hostname] = 'NoSchedule'

        elif resource == 'load':
            if dict_info_json[resource]['min5'] > 80:

                LOAD_OK = False

                logger.warning(
                    f'Load average at 5min in node {hostname} is over 80%: Load(min5) % = {dict_info_json[resource]["min5"]} %')

                # Check if node is already tainted
                if hostname in taints.keys():
                    logger.info(
                        f'Node {hostname} is already tainted as {taints[hostname]}')
                # If not tainted, taint the node
                else:
                    logger.info(
                        f'Tainting node {hostname} to avoid scheduling of any other containers')

                    taints[hostname] = 'NoSchedule'

    # Untaint the node if everything is OK
    if CPU_OK and MEM_OK and LOAD_OK and hostname in taints.keys():
        taints.pop(hostname)
        logger.info(
            f'Node {hostname} untainted. All parameters are below critical tresholds.')

    return taints


def apply_taints(hostname, resources, dict_info_json, taints, logger):

    new_taints = taint_nodes(
        taints, hostname, resources, dict_info_json, logger)

    return new_taints
