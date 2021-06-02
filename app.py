from os import sep
import signal
import sys
import psutil
import pandas as pd
from typing import Union


class App:

    __process_manager: object

    def __init__(self):
        signal.signal(signal.SIGINT, self.signalHandler)
        self.__process_manager(FileLoader.loadFile("ProgramList.txt"))

    def signalHandler(self, sig, frame):
        self.stop()
        print('Exiting!')
        sys.exit(0)

    def start(self):

        # init miner

        # check processlist

        # start daemon checker

        signal.pause()

    def stop(self):
        ...


class FileLoader:
    def loadFile(file: str) -> list[str]:
        return pd.read_csv(file, header=None)


class ProcessSearcher:
    _process_list: set[str]
    process_list = property(_process_list)

    def __init__(self, process_list: Union[list, set, str] = None):
        self._process_list = set(process_list)

    def searchInList(self) -> bool:
        for p in psutil.process_iter():
            if p.name().lower() in self._process_list:
                return True
        return False


class Miner:
    __filepath: str
    __process: psutil.Process
    filepath = property(__filepath)

    def start():
        psutil


if __name__ == "__main__":
    app = App()
    app.start()
