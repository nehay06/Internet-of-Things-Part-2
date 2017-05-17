import Pyro4
import sys
sys.path.append('/Users/nehayadav/spring17-lab3-nyadav66')
from src.constants.Constants import Constants
from src.sensor.Sensor import Sensor

daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()
Sensor(daemon, nameServer, None, Constants.ProcessNames.PROCESS_FIRE)

print("Sensor Fire registered.")

daemon.requestLoop()