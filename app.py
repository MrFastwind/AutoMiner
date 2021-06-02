from os import sep
import signal
import sys
import psutil
import subprocess
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
    __args: list[str]
    __process: subprocess.Popen
    __alive: bool = False
    filepath = property(__filepath)
    args = property(__args)
    alive = property(__alive)

    def __init__(self, file: str, args: list):
        self.__filepath, self.__args = file, args

    def start(self):
        self.__process = subprocess.Popen(
            executable=self.__filepath, args=self.__args)

    def stop(self):
        if self.alive:
            self.__process.terminate()
            self.__alive = False

    def kill(self):
        if self.alive:
            self.__process.kill()
            self.__alive = False


if __name__ == "__main__":
    app = App()
    app.start()
