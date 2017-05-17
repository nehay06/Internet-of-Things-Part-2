import Pyro4
import sys
sys.path.append('/Users/nehayadav/spring17-lab3-nyadav66')
from src.constants.Constants import Constants
from src.loadBalancer.LoadBalancer import LoadBalancer


daemon = Pyro4.Daemon()

# finds the name server
nameServer = Pyro4.locateNS()
LoadBalancer(daemon,nameServer,Constants.Loadbalancer.NAME)

print("Load Balancer registered.")
daemon.requestLoop()