import time
import pathlib
import signal
import sys
import threading
from pathlib import Path
from miners import Miner, GeneralMiner
from resourcemanager.FileLoader import FileLoader, ProgamListLoader
from process import ProcessListUpdater, ProcessSearcher

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
        self.__listupdater = ProcessListUpdater(LISTFILE)
        self.__process_searcher = ProcessSearcher(
            FileLoader.loadFile(LISTFILE))
        self.__miner:Miner = GeneralMiner(executable=DIRPATH / FILEPATH, args=ARGS)
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


if __name__ == "__main__":
    app = App()
    app.start()
