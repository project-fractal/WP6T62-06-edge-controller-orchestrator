class Orchestrator:
    'The Orchestrator class provides methods to communicate with the custom orchestrator API'

    def __init__(self, custom_orchestrator):
        self.hostname = custom_orchestrator['hostname']
        self.ip = custom_orchestrator['IP']
        self.port = custom_orchestrator['port']

    def send_taints(taints):
        return
