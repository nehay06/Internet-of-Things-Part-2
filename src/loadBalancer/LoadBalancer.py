import Pyro4

@Pyro4.expose
class LoadBalancer:

    def __init__(self,daemon, nameServer, processname):
        """
        Initializes the Load balancer
        webserverload is a map of server load : WS -> load
        webserverProcesses is a map of webserver and its processes: WS -> [list of processes]
        webseverlist is a list of available webservsers: [list of WS available]
        """
        self.webserverLoad = {}
        self.webserverProcesses = {}
        self.availableWebserverlist = []
        self.processName = processname
        self._registerOnserver(daemon, nameServer)


    def assignWebserver(self, processname):
        """
        Assigns webserver to any process
        :param processname: process name to identify
        :return: webserver process name
        """
        ws = min(self.webserverLoad, key=self.webserverLoad.get)    # find the least loaded server
        self.webserverLoad[ws] += 1                                 # increase its load
        processList = self.webserverProcesses[ws]
        processList.append(processname)                             # add this process to ws list
        self.webserverProcesses[ws] = processList

        print("Assigning {} to {}".format(processname,ws))
        proxyName = "PYRONAME:" + processname                       # notify the process of the new reporting weberver it has
        processProxy = Pyro4.Proxy(proxyName)
        processProxy.changeWebServer(ws)


    def reportDeadWebserver(self, webserver):
        """
        Removes webserver from dictionary. Or none if no key found.
        :param webserver: webserver process name
        :return: None
        """
        print("Alert!! Dead Server Reported {}".format(webserver))
        self.webserverLoad.pop(webserver, None)                     # remove the weberver from the webserver load dictionary
        processList = self.webserverProcesses[webserver]            # obtain the processes registered on this dead webserver
        if webserver in self.availableWebserverlist:
            self.availableWebserverlist.remove(webserver)           # remove the webserver from the available weberver list

        for process in processList:                                 # assign a new webserver to these processes
            self.assignWebserver(process)

        self.webserverProcesses.pop(webserver, None)


    def addWebserver(self, webserver):
        """
        Adds a webserver to the list
        :param webserver: webserver process name
        :return: None
        """
        self.webserverLoad[webserver] = 0
        self.webserverProcesses[webserver] = []
        self.availableWebserverlist.append(webserver)
        print ("Adding webserver {}".format(webserver))


    def _registerOnserver(self, daemon, nameserver):
        """
        Registering on Pyro Server.
        :param daemon: the daemon process.
        :param nameserver: the nameServer.
        :return: None
        """
        uri = daemon.register(self)
        nameserver.register(self.processName, uri)
        print("LoadBalancer registered. Name {} and uri {} ".format(self.processName, uri))

    def getWebServerList(self):
        return self.availableWebserverlist