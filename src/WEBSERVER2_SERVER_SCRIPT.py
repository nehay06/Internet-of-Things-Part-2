import Pyro4
import sys
sys.path.append('/Users/nehayadav/spring17-lab3-nyadav66')
from src.constants.Constants import Constants
from src.webServer.WebServer import WebServer

daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()
webserver = WebServer(daemon, nameServer, Constants.ProcessNames.PROCESS_WEBSERVER_2, Constants.Loadbalancer.NAME)
print("Webserver 2 registered.")

daemon.requestLoop()