import Pyro4

from src.constants.Constants import Constants
import random
from time import time
import timeit
from collections import deque, defaultdict


@Pyro4.expose
class FrontEnd:
    def __init__(self, backend, webservername):
        """
        Front End class which manages cache operations and accesses backend to write into database.
        :param backend:
        :param webservername:
        """

        self.webservername = webservername
        #self.registerProcesses.append(webservername)
        self.processToFileMap = {}                                  # process name and its correspondong filename
        # Private members
        self._backend = backend
        self.registerdProcesses = []
        self.cacheCapacity = 5                                      # Capacity of cache
        self.cache = defaultdict(list)

    def initializeCache(self,cacheCapacity,processList):
        """
        Initialize the cache. Cache is write-through.
        :param cacheCapacity: The cache capacity.
        :return: None
        """
        self.cacheCapacity = cacheCapacity
        print("Initializing the cache and processNames are : {}".format(processList))
        for key in processList:
            self.cache[key] = deque([], self.cacheCapacity)
        
        print("Items in {} cache {}".format(self.webservername,self.cache))


    def registerProcesses(self, processname):
        """
        The incoming new process registers itself through this.
        A new database file is created.
        :param processname: The process to be reigstered.
        :return: None
        """
        self.registerdProcesses.append(processname)
        filepath = Constants.FileConstants.FILE_DIR + self.webservername + processname + ".txt"
        self._backend.createFile(filepath)
        self.processToFileMap[processname] = filepath


    def getData(self, processname, requestedCount):
        """
        Checks cache if the requsted recent entries are found.
        If not, then database is queried.
        :param processname: process for which entries are requested
        :param requestedCount: The latest count of entries.
        :return: The entries
        """
        def getKey(item):
            return item[0]
        print("Current Information in cache is {}".format(self.cache))
        print()
        if requestedCount <= self.cacheCapacity and len(self.cache[processname])  >= requestedCount:
            t0 = time()
            print("Information found in Cache")
            data = list(self.cache[processname])
            print("Top {} records for {} from cache are {}".format(requestedCount,processname,data[:requestedCount]))
            print("Time to fetch the information is {}".format(time()-t0))
            return data[:requestedCount]
        else:
            print("Information not in Cache fetching from database")
            t0 = time()
            result = self._backend.readFromFile(self.processToFileMap[processname], requestedCount)
            print("Requested information is {}".format(result))
            print()
            print("Now toring the requested information in cache")
            print()
            self.cache[processname].clear()
            sortedData = sorted(result, key=getKey)
            for index in range(self.cacheCapacity):
                if index < len(sortedData):
                    self.cache[processname].append([sortedData[index][0], sortedData[index][1]])
            print("Time to fetch the information is {}".format(time()-t0))

    def pushData(self, processname, state, logtime):
        """
        The new data is written into database first.
        Then its written into cache.
        :param processname:
        :param state:
        :param logtime:
        :return:
        """
        print("Contacting Backend to push state for {}".format(processname))
        string = str(logtime) + "," + str(processname )+ "," + str(state)+"\n"
        if processname not in self.processToFileMap:
            # create a new file
            filepath = Constants.FileConstants.FILE_DIR + self.webservername + processname + ".txt"
            self._backend.createFile(filepath)
            self.processToFileMap[processname] = filepath
        
        filepath = self.processToFileMap[processname]

        if self._backend.writeToFile(string, filepath):
            print("Writing information to cache for {}".format(processname))
            self.writeCache(processname, [str(logtime), str(state)])

    def writeCache(self, processname, data):
        """
        Writes data to cache of the process
        :param processname: The processname
        :param data: The data to be written
        :return:
        """
        if self.cache[processname] and len(self.cache[processname]) == self.cacheCapacity :
            self.cache[processname].pop()      
        self.cache[processname].appendleft(data)





