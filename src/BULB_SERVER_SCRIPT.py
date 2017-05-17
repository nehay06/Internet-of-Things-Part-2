import Pyro4
import sys
sys.path.append('/Users/nehayadav/spring17-lab3-nyadav66')
from src.constants.Constants import Constants
from src.device.Device import Device

daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()
Device(daemon, nameServer, None, Constants.ProcessNames.PROCESS_BULB)

print("Device Bulb registered.")

daemon.requestLoop()