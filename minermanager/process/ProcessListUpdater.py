from resourcemanager import ProgamListLoader 
import time
import os

class ProcessListUpdater():

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
            self._programs = ProgamListLoader.loadFile(self.__file)

    def _getList(self):
        if self.isChanged():
            self._update()
        return self._programs

    def isChanged(self):
        mtime = os.stat(self.__file).st_mtime
        return self._lastupdate != mtime, mtime