from abc import ABC, abstractmethod

class CloudProvider(ABC):
    def __init__(self):
        self.pricing_data = []
    
    @abstractmethod
    def get_pricing(self):
        """Get pricing data for the cloud provider"""
        pass
    
    @abstractmethod
    def update_pricing(self):
        """Update pricing data from the provider's API"""
        pass 