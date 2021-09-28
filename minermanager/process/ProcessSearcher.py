import psutil
from typing import Union

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
