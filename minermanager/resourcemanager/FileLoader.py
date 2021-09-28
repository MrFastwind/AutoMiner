from abc import ABC, abstractmethod
import pandas as pd

class FileLoader(ABC):
    @abstractmethod
    @classmethod
    def loadFile(file:str) -> list[str]:
        pass


class ProgamListLoader(FileLoader):
    @classmethod
    def loadFile(file: str) -> list[str]:
        return set(pd.read_csv(file, header=None).values.flat)
