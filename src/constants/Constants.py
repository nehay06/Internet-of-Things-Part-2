

class Constants:

    class FileConstants:
        FILE_DIR = './'

    class SensorConstants:
        STATE_OFF = "OFF"
        STATE_ON = "ON"


    class DeviceConstants:
        STATE_OFF = "OFF"
        STATE_ON ="ON"

    class WebserverConstants:
        STATE_ALIVE = "ALIVE"
        STATE_DEAD = "DEAD"

    class ServerConstants:
        PYRONAME = "PYRONAME:"
        SERVER_HOST = "localhost"
        SERVER_PORT = 9090


    class ProcessNames:
        PROCESS_BULB = "BULB"
        PROCESS_DOOR = "DOOR"
        PROCESS_MOTION = "MOTION"
        PROCESS_FIRE = "FIRE"
        PROCESS_WEBSERVER_1 = "WEBSERVER_1"
        PROCESS_WEBSERVER_2 = "WEBSERVER_2"
        PROCESS_WEBSERVER_3 = "WEBSERVER_3"
        MANAGER = "MANAGER"

    class Loadbalancer:
        NAME = "LOADBALANCER"

    class MessageConstants:
        INITIATE_ELECTION = "INITIATE_ELECTION"
        ELECTION = "ELECTION"
        OK  = "OK"


