from  abc import ABC, abstractmethod
from dataclasses import dataclass
from os import name
from typing import Dict, List

class Process(ABC):

    @property
    @abstractmethod
    def alive(self):
        pass
    
    @abstractmethod
    def start(self):
        """Start the process"""      
        pass

    @abstractmethod
    def stop(self):
        """Stop the process"""
        pass

    @abstractmethod
    def kill(self):
        """Force the closing of the process"""
        pass

class Miner():
    
    
    @abstractmethod
    def __init__(self):
        pass
    
    @property
    @abstractmethod
    def config() -> Dict:
        pass
    
    pass

@dataclass
class MinerWorker:
    wallet: hex 
    name: str = 'worker'
    
    def __str__(self):
        return f'{self.wallet}.{self.name}'

@dataclass
class MinerPool:
    address: str
    port: str
    algo: str

