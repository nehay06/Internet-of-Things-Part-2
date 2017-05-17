import Pyro4
import sys
sys.path.append('/Users/nehayadav/spring17-lab3-nyadav66')
from src.constants.Constants import Constants
from src.sensor.Sensor import Sensor
from src.device.Device import Device
from src.webServer.WebServer import WebServer
from src.loadBalancer.LoadBalancer import LoadBalancer


# Initializing Pyro Names of eachof the registered processes

webServer1 = Constants.ProcessNames.PROCESS_WEBSERVER_1
webServer2 = Constants.ProcessNames.PROCESS_WEBSERVER_2
webServer3 = Constants.ProcessNames.PROCESS_WEBSERVER_3
LoadBalancer = Constants.Loadbalancer.NAME
fire = Constants.ProcessNames.PROCESS_FIRE
motion= Constants.ProcessNames.PROCESS_MOTION
door = Constants.ProcessNames.PROCESS_DOOR
bulb = Constants.ProcessNames.PROCESS_BULB
manager = Constants.ProcessNames.MANAGER

processList = [motion,door,bulb,fire]
cacheCapacity = 5


# Adding server to LoadBalancer Records

LoadBalancerURI = "PYRONAME:"+LoadBalancer
loadbalancerProxy = Pyro4.Proxy(LoadBalancerURI)
loadbalancerProxy.addWebserver(webServer1)
loadbalancerProxy.addWebserver(webServer2)
loadbalancerProxy.addWebserver(webServer3)

webServer1URI = "PYRONAME:"+webServer1
webServer2URI = "PYRONAME:"+webServer2
webServer3URI = "PYRONAME:"+webServer3

#Elect Leader amonf webserver
print("---------------------------------------------------------------------------------")
print("Leader Election")
proxyObj = Pyro4.Proxy(webServer3URI)
proxyObj.triggerElection(Constants.MessageConstants.INITIATE_ELECTION,[webServer1,webServer2,webServer3],manager)
webServers = [webServer1,webServer2,webServer3]

Leader = None
for WebServer in webServers:
	uri = "PYRONAME:"+WebServer
	proxyObj = Pyro4.Proxy(uri)
	if (proxyObj.getLeader()):
		Leader = WebServer
		print("Elected Leader is {}".format(Leader))
print("Leader Election Process Completed")

loadbalancerProxy.setLeader(Leader)


# Webservers pulling information about their peers from LoadBalancer

webserver1Name = "PYRONAME:" + webServer1 
webserver1Proxy = Pyro4.Proxy(webserver1Name)
webserver1Proxy.getPeerWebserversList()
webserver1Proxy.updateEligibleStatus()

webserver2Name = "PYRONAME:" + webServer2 
webserver2Proxy = Pyro4.Proxy(webserver2Name)
webserver2Proxy.getPeerWebserversList()
webserver2Proxy.updateEligibleStatus()

webserver3Name = "PYRONAME:" + webServer3 
webserver3Proxy = Pyro4.Proxy(webserver3Name)
webserver3Proxy.getPeerWebserversList()
webserver3Proxy.updateEligibleStatus()

# Dynamically assigning processes their webservers

loadbalancerProxy.assignWebserver(motion)
loadbalancerProxy.assignWebserver(door)
loadbalancerProxy.assignWebserver(fire)

# Initializing cache of the webservers

print("Contacting Webserver 1 and initializing it's cache")
webServer1URI = "PYRONAME:"+webServer1
proxywebServer1 = Pyro4.Proxy(webServer1URI)
proxywebServer1.cacheInitialize(cacheCapacity,processList)
	

print("Contacting Webserver 2 and initializing it's cache")
webServer2URI = "PYRONAME:"+webServer2
proxywebServer2 = Pyro4.Proxy(webServer2URI)
proxywebServer2.cacheInitialize(cacheCapacity,processList)


print("Contacting Webserver 3 and initializing it's cache")
webServer3URI = "PYRONAME:"+webServer3
proxywebServer3 = Pyro4.Proxy(webServer3URI)
proxywebServer3.cacheInitialize(cacheCapacity,processList)





