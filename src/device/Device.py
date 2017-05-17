import Pyro4
from src.constants.Constants import Constants
import time

@Pyro4.expose
class Device:

    def __init__(self, daemon, nameServer, webServer, processName):
        """
        The device class is initialized here.
        :param daemon: The daemon background process.
        :param nameServer: The Pyro nameserver
        :param webServer: The webserver to register. Initially None.
        :param processName: The self processs name
        """
        self.state = Constants.DeviceConstants.STATE_OFF
        self.processName = processName

        # Private members

        self._webServer = None
        self._registerOnserver(daemon, nameServer)


    def changeWebServer(self, new_webserver):
        """
        Function to change the reporting webserver
        :param new_webserver: The new reporting webserver
        :return: None
        """
        self._webServer = new_webserver
        print "Now ", self.processName, " registering with : ", self._webServer
        self.registerOnWebServer()
        print "Congrats! You are ", self.processName, " and registered with : ", self._webServer



    def registerOnWebServer(self):
        """
        Calls the reporting webserver to register itself on it.
        :return: None
        """
        proxyName = "PYRONAME:" + self._webServer
        webServerProxy = Pyro4.Proxy(proxyName)
        print("Registering {} with Webserver: {} and WebserverProxy: {}".format(self.processName, proxyName, webServerProxy))
        webServerProxy.registerOnWebServer(self.processName)


    def pushState(self):
        """
        Pushes its own state to reporting webserver.
        :return: None
        """
        proxyName = "PYRONAME:" + self._webServer
        webServerProxy = Pyro4.Proxy(proxyName)
        print("Modified State is {}".format(self.state))
        curtime = time.time()
        retval = webServerProxy.pushState(self.processName, self.state,curtime, self.processName)
        if retval == True:
            print self.processName, " succesfully pushed state to servers"

    def pullState(self):
        """
        Function to pull state
        :return: current timestamp, state
        """
        curtime = time.time()
        return curtime, self.state

    def changeState(self):
        """
        Change the current state of the process.
        :return: None
        """
        print("Current State is {}".format(self.state))
        if self.state == Constants.DeviceConstants.STATE_OFF:
            self.state = Constants.DeviceConstants.STATE_ON
        else:
            self.state = Constants.DeviceConstants.STATE_OFF

    def _registerOnserver(self, daemon, nameserver):
        """
        Registering on Pyro Server.
        :param daemon: the daemon process.
        :param nameserver: the nameServer.
        :return: None
        """
        uri = daemon.register(self)
        nameserver.register(self.processName, uri)
        print("Sensor registered. Name {} and uri {} ".format(self.processName, uri))
        pass