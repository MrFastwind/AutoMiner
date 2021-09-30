from abc import ABC, abstractclassmethod, abstractmethod, abstractstaticmethod
from dataclasses import dataclass
import yaml
import pathlib

@dataclass
class Worker:
    wallet: hex = 0x0
    name: str = "worker"

@dataclass
class Pool:
    address: str
    port: int

@dataclass
class Miner:
    type: type
    executable: str
    additional_args: str

@dataclass
class Config:
    worker: Worker
    pool: Pool
    miner: Miner

class ConfigLoader(ABC):
    
    _CONFIG_FILE: str = pathlib.Path.home() / ".minermanager"
    
    @abstractclassmethod
    def getConfig(worker: str, pool: str, miner: str) -> Config:
        pass
    
    @abstractstaticmethod
    def LoadFile( path: str) -> dict:
        pass


class YAMLConfigLoader(ConfigLoader):
    
    @classmethod
    def getConfig(worker: str, pool: str, miner: str) -> Config:
        data = YAMLConfigLoader.LoadFile(YAMLConfigLoader._CONFIG_FILE)
        return Config(
            Worker(data["workers"]["profiles"][worker]),
            Pool(data["pools"]["profiles"][pool]),
            Miner(data["miners"]["profiles"][miner]))
        
    @staticmethod
    def LoadFile( path: str) -> dict:
        return dict(yaml.load(open( path, "r")))