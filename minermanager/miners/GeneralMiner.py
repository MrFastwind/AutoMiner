import Miner
import subprocess
from typing import Union, Tuple
from pathlib import Path

class GeneralMiner(Miner):
    __filepath: str
    __args: list[str]
    __process: subprocess.Popen = None
    __return_code: int

    executable = property(lambda self: self.__filepath)
    args = property(lambda self: self.__args)

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

    @property
    def alive(self) -> bool:
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
