from  abc import ABC, abstractmethod

class Miner(ABC):

    @property
    @abstractmethod
    def alive(self):
        pass
    
    @abstractmethod
    def start(self):
        """Start the miner"""      
        pass

    @abstractmethod
    def stop(self):
        """Stop the miner"""
        pass

    @abstractmethod
    def kill(self):
        """Force the closing of the miner"""
        pass