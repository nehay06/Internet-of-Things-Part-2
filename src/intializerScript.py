import Pyro4
import sys
sys.path.append('/Users/nehayadav/spring17-lab3-nyadav66')
from src.constants.Constants import Constants
from src.sensor.Sensor import Sensor
from src.device.Device import Device
from src.webServer.WebServer import WebServer
from src.loadBalancer.LoadBalancer import LoadBalancer
import random


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
cacheCapacity = 5

processList = [motion,door,bulb,fire]

# Adding server to LoadBalancer Records

LoadBalancerURI = "PYRONAME:"+LoadBalancer
loadbalancerProxy = Pyro4.Proxy(LoadBalancerURI)
loadbalancerProxy.addWebserver(webServer1)
loadbalancerProxy.addWebserver(webServer2)

# Webservers pulling information about their peers from LoadBalancer

webserver1Name = "PYRONAME:" + webServer1 
webserver1Proxy = Pyro4.Proxy(webserver1Name)
webserver1Proxy.getPeerWebserversList()

webserver2Name = "PYRONAME:" + webServer2 
webserver2Proxy = Pyro4.Proxy(webserver2Name)
webserver2Proxy.getPeerWebserversList()

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

