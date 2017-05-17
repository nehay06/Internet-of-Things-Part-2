import Pyro4
import sys
sys.path.append('/Users/nehayadav/spring17-lab3-nyadav66')
from src.constants.Constants import Constants
from src.sensor.Sensor import Sensor
from src.device.Device import Device
from src.webServer.WebServer import WebServer

webServer1 = Constants.ProcessNames.PROCESS_WEBSERVER_1
webServer2 = Constants.ProcessNames.PROCESS_WEBSERVER_2
fire = Constants.ProcessNames.PROCESS_FIRE
motion= Constants.ProcessNames.PROCESS_MOTION
door = Constants.ProcessNames.PROCESS_DOOR
bulb = Constants.ProcessNames.PROCESS_BULB

fireURI = "PYRONAME:"+fire
proxyFire = Pyro4.Proxy(fireURI)

motionURI = "PYRONAME:"+motion
proxyMotion = Pyro4.Proxy(motionURI)

doorURI = "PYRONAME:"+door
proxyDoor = Pyro4.Proxy(doorURI)

bulbURI = "PYRONAME:"+bulb
proxyBulb = Pyro4.Proxy(bulbURI)


webServer1URI = "PYRONAME:"+webServer1
proxywebServer1 = Pyro4.Proxy(webServer1URI)
#proxywebServer1.startHeartBeatThread()

	
webServer2URI = "PYRONAME:"+webServer2
proxywebServer2 = Pyro4.Proxy(webServer2URI)


proxyMotion.chageState()
proxyMotion.pushState()

proxyDoor.chageState()
proxyDoor.pushState()

proxyDoor.chageState()
proxyDoor.pushState()

proxyFire.chageState()
proxyFire.pushState()

proxyDoor.chageState()
proxyDoor.pushState()

proxyMotion.chageState()
proxyMotion.pushState()

proxyDoor.chageState()
proxyDoor.pushState()

proxyDoor.chageState()
proxyDoor.pushState()

proxyMotion.chageState()
proxyMotion.pushState()

proxyDoor.chageState()
proxyDoor.pushState()

proxyDoor.chageState()
proxyDoor.pushState()

