from discovery_agent import DiscoveryAgent
from negotiation_agent import NegotiationAgent
from communication_agent import CommunicationAgent
from documentation_agent import DocumentationAgent

class MultiAgentController:
    def __init__(self):
        self.discovery = DiscoveryAgent()
        self.negotiation = NegotiationAgent()
        self.communication = CommunicationAgent()
        self.documentation = DocumentationAgent()
