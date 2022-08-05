import requests


class Orchestrator:
    'The Orchestrator class provides methods to communicate with the custom orchestrator API'

    def __init__(self, custom_orchestrator):
        self.hostname = custom_orchestrator['hostname']
        self.ip = custom_orchestrator['IP']
        self.port = custom_orchestrator['port']

    def send_taints(self, taints):
        RESOURCE = '/api/v1/update_taints'

        URL = 'http://' + str(self.ip) + ':' + str(self.port) + RESOURCE

        requests.post(url=URL, json=taints)

    def load_nodes_info(self, **kwargs):
        RESOURCE = '/api/v1/load_nodes'

        URL = 'http://' + str(self.ip) + ':' + str(self.port) + RESOURCE

        if kwargs['resources']:
            requests.post(
                url=URL, json=kwargs)
        else:
            requests.post(
                url=URL, json=kwargs)
