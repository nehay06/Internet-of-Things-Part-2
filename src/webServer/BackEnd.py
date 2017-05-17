from lockfile import LockFile, LockTimeout
import os

class BackEnd:

    def __init__(self):
        pass


    def createFile(self, filepath):
        if not os.path.isfile(filepath):
            file = open(filepath, "w")
            file.close()
            return True
        return False


    def readFromFile(self, filepath, numRows):
        lock = LockFile(filepath)
        while not lock.i_am_locking():
            try:
                lock.acquire(timeout=60)  # wait up to 60 seconds
            except LockTimeout:
                lock.break_lock()
                lock.acquire()
        if not os.path.isfile(filepath):
            file = open(filepath, "w")
        else:
            file = open(filepath, "a")
        output = []
        counter = 1
        for line in reversed(open(filepath).readlines()):
            stringData = line.rstrip().split(",")
            if counter <= numRows:
                output.append(stringData)
                counter += 1
            else:
                break
        file.close()
        lock.release()
        return output


    def writeToFile(self, data, filepath):
        print("Writing data the database")
        lock = LockFile(filepath)
        while not lock.i_am_locking():
            try:
                lock.acquire(timeout=60)  # wait up to 60 seconds
            except LockTimeout:
                lock.break_lock()
                lock.acquire()
        if not os.path.isfile(filepath):
            file = open(filepath, "w")
        else:
            file = open(filepath, "a")
        file.write(data)
        file.close()
        lock.release()
        return True





