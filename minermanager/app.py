import os
import pathlib
import signal
import subprocess
import sys
import threading
import time
from os import sep
from pathlib import Path
from typing import Tuple, Union

import pandas as pd
import psutil

DIRPATH = Path("D:\Mining\lolMiner")
FILEPATH = Path("lolMiner.exe")
ARGS = ("--algo", "ETCHASH", "--pool", "eu1-etc.ethermine.org:4444", "--user", "0x1e3543b1845c418668cE20FE2eaB28484A6B8d1B.PC-Miner")
LISTFILE = pathlib.Path("ProgramList.txt")


class App:

    __alive: bool
    __sleep_time: int
    alive = property(lambda self: self.__alive)

    def __init__(self):
        signal.signal(signal.SIGINT, lambda sig, frame: self.signalHandler())
        self.__listupdater = ProgramListUpdater(LISTFILE)
        self.__process_searcher = ProcessSearcher(
            FileLoader.loadFile(LISTFILE))
        self.__miner = Miner(executable=DIRPATH / FILEPATH, args=ARGS)
        self.__thread_checker = threading.Thread(target=self.checker)
        self.__alive = False
        self.__sleep_time = 1

    def signalHandler(self):
        self.stop()
        print('Exiting!')
        sys.exit(0)

    def start(self):
        self.__alive = True
        self.__thread_checker.start()
        while self.alive:
            time.sleep(0.5)
        # signal.pause()

    def checker(self):
        while self.__alive:
            # updates list of programs
            self.__process_searcher.process_list = self.__listupdater.programs

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
        return set(pd.read_csv(file, header=None).values.flat)


class ProgramListUpdater():

    _lastupdate: float = 0
    _programs: set[str]
    last_update = property(lambda self: time.ctime(self._lastupdate))
    programs = property(lambda self: self._getList())

    def __init__(self, file: str):
        self.__file = file

    def _update(self):
        # time.ctime(os.stat(self.__file)[os.stat.ST_MTIME])
        result, last_mtime = self.isChanged()
        if result:
            self._lastupdate = last_mtime
            self._programs = FileLoader.loadFile(self.__file)

    def _getList(self):
        if self.isChanged():
            self._update()
        return self._programs

    def isChanged(self):
        mtime = os.stat(self.__file).st_mtime
        return self._lastupdate != mtime, mtime


class ProcessSearcher:
    _process_list: set[str]
    process_list = property(lambda self: self._process_list,
                            fset=lambda self, value: self.__listToSet(value))

    def __init__(self, process_list: Union[list, set, str] = []):
        self._process_list = self.__listToSet(process_list)

    def __listToSet(self, process_list):
        return {proc.lower() for proc in process_list}

    def searchInList(self) -> bool:
        return any(
            p.name().lower() in self._process_list for p in psutil.process_iter()
        )


class Miner:
    __filepath: str
    __args: list[str]
    __process: subprocess.Popen = None
    __return_code: int

    executable = property(lambda self: self.__filepath)
    args = property(lambda self: self.__args)
    alive = property(lambda self: self.isAlive())

    def __init__(self, args:Union[list[str],Tuple], executable: Union[str,Path]=None):
        """Miner constructor.

        Args:
            args (Union[list[str],Tuple]): List of arguments to pass at the Miner
            executable (Union[str,Path], optional): Executable to use for the miner, if None it will use the first element of args. Defaults to None.

        Raises:
            ValueError: if args and executable are not set.
        """
        
        if not args and not executable:
            raise ValueError()

        args = list(args)

        executable = args.pop(0) if not executable else str(executable)
        self.__filepath, self.__args = executable, args
    
    def __cmd(self):
        return [self.__filepath] + self.__args

    def start(self):
        self.__process = subprocess.Popen(args=self.__cmd(), stdin=subprocess.DEVNULL)

    def stop(self):
        if self.alive:
            self.__process.terminate()

    def kill(self):
        if self.alive:
            self.__process.kill()

    def isAlive(self) -> bool:
        if self.__process is None:
            return False
        if not self.getReturnCode():
            return True
        return False

    def getReturnCode(self):
        if self.__process is None:
            return None
        self.__return_code = self.__process.poll()
        return self.__return_code


if __name__ == "__main__":
    app = App()
    app.start()
