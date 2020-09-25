import logging
from collections import deque
import sys
from threading import Lock
import glob
import os
from os.path import isfile, join
from os import listdir
from _datetime import datetime


class LogStream(object):
    def __init__(self, maxlines = 1000):
        self.maxlines = maxlines
        self.logbuf = deque(maxlen=maxlines)
        self.logbuf_lock = Lock()

    def write(self, data):
        with self.logbuf_lock:
            if len(data) > 1:
                self.logbuf.append(data)

        return sys.stderr.write(data)

    def get(self, nmax=None, remove=False):
        if nmax is None:
            nmax = sys.maxsize

        if nmax == 0:
            return []

        res = []
        with self.logbuf_lock:
            if remove is True:
                _list = self.logbuf
            else:
                _list = self.logbuf.copy()

            if nmax > 0:
                method = _list.pop
                left = nmax
            else:
                method = _list.popleft
                left = -nmax

            for n in range(left):
                try:
                    res.append(method())
                except IndexError:
                    break

            if nmax > 0:
                res[:] = reversed(res)

        return res

    def flush(self):
        return sys.stderr.flush()

class LogFile(object):
    def __init__(self, maxlines = 1000):
        self.maxlines = maxlines
        self.logbuf = deque(maxlen=maxlines)
        self.logbuf_lock = Lock()
        
        logpath = "/home/pi/e/"
        try:
            if not os.path.exists(logpath):
                os.makedirs(logpath)
        except:
             logpath = "e/"
        logfileNumber = 1
        # find new logfile number
        logfiles = listdir(logpath)
        
        for lf in logfiles:
            if isfile(join(logpath, lf)):
                lfnr = int(lf[0:8])
                if lfnr>=logfileNumber:
                    logfileNumber = lfnr+1
        logfilename = '{0:08d}'.format(logfileNumber)+"-e.log"

        self.logfile = open(logpath+logfilename,"w+")
        
    def write(self, data):
        with self.logbuf_lock:
            if len(data) > 1:
                self.logbuf.append(data)
        
        # write to logfile
        #self.logfile.write(data)
#TODO: do not flush ervery time??!!
        #self.logfile.flush()
        
        return sys.stderr.write(data)

    def get(self, nmax=None, remove=False):
        if nmax is None:
            nmax = sys.maxsize

        if nmax == 0:
            return []

        res = []
        with self.logbuf_lock:
            if remove is True:
                _list = self.logbuf
            else:
                _list = self.logbuf.copy()

            if nmax > 0:
                method = _list.pop
                left = nmax
            else:
                method = _list.popleft
                left = -nmax

            for n in range(left):
                try:
                    res.append(method())
                except IndexError:
                    break

            if nmax > 0:
                res[:] = reversed(res)

        return res

    def flush(self):
        #self.logfile.flush()
        return sys.stderr.flush()


logstreambuf = LogStream()
#logfilebuf = LogFile()

log = logging.getLogger("somelog")
log.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

#handler = logging.StreamHandler(logfilebuf)
handler = logging.StreamHandler(logstreambuf)
handler.setFormatter(formatter)

log.addHandler(handler)
