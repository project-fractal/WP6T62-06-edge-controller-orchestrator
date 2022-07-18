import kubernetes
import docker


class UnsupportedOrchestratorException(Exception):
    def __init__(self, hostname, orchestrator):
        self.hostname = hostname
        self.orchestrator = orchestrator
        self.message = f'The Orchestrator {orchestrator} for node {hostname} is not supported'
        super().__init__(self.message)


def actions(node, orchestrator, resources, dict_info_json):

    if orchestrator == 'kubernetes':
        pass
        # TODO: Take actions for Kubernetes
    elif orchestrator == 'docker':
        pass
        # TODO: Take actions for Docker
    else:
        raise UnsupportedOrchestratorException(node, orchestrator)
    taken_actions = []

    return taken_actions
