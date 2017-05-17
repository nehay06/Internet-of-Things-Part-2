import Pyro4
import time
import thread, threading
from multiprocessing.pool import ThreadPool
import sys
import random
sys.path.append('/Users/nehayadav/spring17-lab3-nyadav66')
from src.constants.Constants import Constants

from src.webServer.FrontEnd import FrontEnd
from src.webServer.BackEnd import BackEnd

@Pyro4.expose
class WebServer:

    # This section consists of initializer functions

    def __init__(self, daemon, nameServer, processname, loadbalancer):
        """
        Constructor for Webserver
        :param daemon: The daemon process
        :param nameServer: The pyronameserver name
        :param processname: Self process name
        :param loadbalancer: The proxy name of Load balancer
        """
        self.STATUS = Constants.WebserverConstants.STATE_ALIVE
        self.loadbalancer = loadbalancer

        # Private members
        self._processname = processname
        self._backEnd = BackEnd()                                       # Create new BackEnd object
        self._frontEnd = FrontEnd(self._backEnd, processname)           # Create new FrontEnd object
        self._registerOnServer(daemon, nameServer)    # register itself on pyro nameserver
        self.eligible = True
        self.leader = False                 


    def cacheInitialize(self,capacity,processList):
        """
        Calls the FrontEnd object to initialize cache
        :param capacity:
        :return:
        """
        self._frontEnd.initializeCache(capacity,processList)


    def getPeerWebserversList(self):
        """
        Calls the LoadBalancer object to generate its peer list
        :return:
        """
        proxyName = "PYRONAME:" + self.loadbalancer
        loadbalancerProxy = Pyro4.Proxy(proxyName)
        self.peerServerlist = loadbalancerProxy.getWebServerList()

        # remove your name from the peer list
        if self._processname in self.peerServerlist:
            self.peerServerlist.remove(self._processname)


    def registerOnWebServer(self, processname):
        """
        Device and Sensor processes can call this function to register themselves on webserver
        :param processname: the caller processname
        :return: None
        """
        self._frontEnd.registerProcesses(processname)


    # These methods are for checking health of the server.

    def startHeartBeatThread(self):
        """
        In a separate thread starts calling out to its peers to check their health.
        :return: None
        """
        thread = threading.Thread(target=self.checkHeartBeat)
        thread.daemon = True
        thread.start()

    def checkHeartBeat(self):
        """
        Every 3 seconds checks the health of its peer servers. This is done by leader in case of RAFT.
        :return: None
        """
        while self.STATUS == Constants.WebserverConstants.STATE_ALIVE:
            failed_server = None
            time.sleep(3)
            print "CHECKING HEARTBEAT"
            for server in self.peerServerlist:
                proxyName = "PYRONAME:" + server
                webServerProxy = Pyro4.Proxy(proxyName)
                status = webServerProxy.getHealthStatus()
                if (status == Constants.WebserverConstants.STATE_DEAD):
                    failed_server = server
                    print failed_server , " is DEAD"
                    self.peerServerlist.remove(server)
                    self.reportDeadServer(server)

         
    def reportDeadServer(self, failedserver):
        """
        In case a server is found dead, the loadbalancer is alerted and all the entries corresponding to the dead process
        are removed.
        :param failedserver: The server that failed/crashed/died.
        :return: None
        """
        proxyName = "PYRONAME:" + self.loadbalancer
        loadbalancerProxy = Pyro4.Proxy(proxyName)
        loadbalancerProxy.reportDeadWebserver(failedserver)


    def getHealthStatus(self):
        """
        Return the activity status of the server.
        :return:
        """
        return self.STATUS


    def killWebServer(self):
        """
        Return the activity status of the server.
        :return:
        """
        self.STATUS = Constants.WebserverConstants.STATE_DEAD


    def getData(self, processname, numRows):
        """
        Request the most recent data corresponding to a process.
        :param processname: The processName of the process for which the entries are requested.
        :param numRows: The most recent numRows which are requested
        :return:
        """
        if (self.STATUS == Constants.WebserverConstants.STATE_DEAD):
            return False

        self._frontEnd.getData(processname, numRows)

    def pushState(self, processname, state, logtime, sender):
        """
        Any device/sensor process can use this method to store their states to database.
        :param processname: the process whose states needs to be saved.
        :param state: The state of the process
        :param logtime: The timestamp
        :param sender: The process who sent this data.
        :return: True if Sucessful/ False if not
        """
        if (self.STATUS == Constants.WebserverConstants.STATE_DEAD):
            return False

        if (sender in self.peerServerlist):
            print "Replicating Entry received from ", sender
            self._frontEnd.pushData(processname, state, logtime)
            return True
        else:
            for peer in self.peerServerlist:
                proxyName = "PYRONAME:" + peer
                peerProxy = Pyro4.Proxy(proxyName)
                peerProxy.pushState(processname, state, logtime, self._processname)

            print("Contacting FrontEnd server to push state for {}".format(processname))
            self._frontEnd.pushData(processname, state, logtime)
            return True


    def _registerOnServer(self, daemon, nameserver):
        """
        Registering on Pyro Server.
        :param daemon: the daemon process.
        :param nameserver: the nameServer.
        :return: None
        """
        uri = daemon.register(self)
        nameserver.register(self._processname, uri)
        print("Webserver registered. Name {} and uri {} ".format(self._processname, uri))


    def getLeader(self):
        if (self.STATUS == Constants.WebserverConstants.STATE_DEAD):
            return False

        return self.leader

    def getEligibleStatus(self):
        if (self.STATUS == Constants.WebserverConstants.STATE_DEAD):
            return False

        return self.eligible

    def updateEligibleStatus(self):
        self.eligible = True

    def triggerElection(self,message,UriArray,callerName):
        if (self.STATUS == Constants.WebserverConstants.STATE_DEAD):
            return False

        if message == Constants.MessageConstants.OK:
            self.eligible = False
            print("{} told {}".format(callerName,message))
        
        if self.eligible == False:
            pass
        else:
            if message == Constants.MessageConstants.ELECTION or message == Constants.MessageConstants.INITIATE_ELECTION:
                print("{} requested {}".format(callerName,message))
                rand =  '{:.2f}'.format(random.random())
                if rand >= .95:
                    if callerName != Constants.ProcessNames.MANAGER:
                        uri = "PYRONAME:"+callerName
                        proxyObj = Pyro4.Proxy(uri)
                        proxyObj.triggerElection(Constants.MessageConstants.OK,UriArray,self._processname)
                        print("I ({}) told OK to {}".format(self._processname,callerName))
                    for process in UriArray:
                        if process != callerName and process != self._processname:
                            uri = "PYRONAME:"+process
                            proxyObj = Pyro4.Proxy(uri)
                            if proxyObj.getEligibleStatus() == True:
                                print("I ({}) requested election to {}".format(self._processname,process))
                                proxyObj.triggerElection(Constants.MessageConstants.ELECTION,UriArray,self._processname)
                    
                    if self.eligible == True:
                        self.leader = True
                else:
                    self.eligible = False
