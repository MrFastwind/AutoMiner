from os import sep
import signal
import sys
import psutil
import subprocess
import threading
import time
from pathlib import Path
import pandas as pd
from typing import Union

FILEPATH = Path("D:\Mining\lolMiner\lolMiner.exe")
ARGS = list(("--config", Path("D:\Mining\lolMiner\lolMiner.cfg"),
            "--algo", "ETCHASH",
             "--pool", "eu1-etc.ethermine.org:4444"))


class App:

    __alive: bool
    __sleep_time: int
    alive = property(lambda self: self.__alive)

    def __init__(self):
        signal.signal(signal.SIGINT, self.signalHandler)
        self.__process_searcher = ProcessSearcher(
            FileLoader.loadFile("ProgramList.txt"))
        self.__miner = Miner(file=FILEPATH, args=ARGS)
        self.__thread_checker = threading.Thread(target=self.checker)
        self.__alive = False
        self.__sleep_time = 30

    def signalHandler(self, sig, frame):
        self.stop()
        print('Exiting!')
        sys.exit(0)

    def start(self):
        self.__alive = True
        self.__thread_checker.start()
        # signal.pause()

    def checker(self):
        while self.__alive:
            if(self.__miner.alive and self.__process_searcher.searchInList()):
                self.__miner.stop()
                print("Miner Stopped!")
            elif(not self.__miner.alive and not self.__process_searcher.searchInList()):
                print("Miner Started!")
                self.__miner.start()
            time.sleep(self.__sleep_time)
        self.__miner.stop()

    def stop(self):
        self.__alive = False
        self.__miner.stop()


class FileLoader:
    def loadFile(file: str) -> list[str]:
        return pd.read_csv(file, header=None)


class ProcessSearcher:
    _process_list: set[str]
    process_list = property(lambda self: self._process_list)

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
    filepath = property(lambda self: self.__filepath)
    args = property(lambda self: self.__args)
    alive = property(lambda self: self.__alive)

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
