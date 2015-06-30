#!/usr/bin/env python
'''Starts/stops the test IOC'''
import os
import subprocess
import time
import gwtests

class IOCControl:
    iocProcess = None
    DEVNULL = None

    def startIOC(self, arglist=None):
        '''Starts the test IOC'''
        childEnviron = os.environ.copy()
        childEnviron['EPICS_CA_SERVER_PORT'] = str(gwtests.iocPort)
        childEnviron['EPICS_CA_ADDR_LIST'] = "localhost"
        childEnviron['EPICS_CA_AUTO_ADDR_LIST'] = "NO"

        if not gwtests.verbose:
            self.DEVNULL = open(os.devnull, 'wb')

        if arglist is None:
            iocCommand = [gwtests.iocExecutable, '-d', 'test.db']
        else:
            iocCommand = [gwtests.iocExecutable]
            iocCommand.extend(arglist)

        if gwtests.verbose:
            print "Starting the IOC using\n", " ".join(iocCommand)
        self.iocProcess = subprocess.Popen(iocCommand, env=childEnviron, stdout=self.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(.5)

    def stop(self):
        '''Stops the test IOC'''
        self.iocProcess.terminate()
        if self.DEVNULL:
            self.DEVNULL.close()


if __name__ == "__main__":
    gwtests.setup()
    print "Running the test IOC in verbose mode for {} seconds".format(gwtests.gwRunDuration)
    gwtests.verbose = True
    iocControl = IOCControl()
    iocControl.startIOC()
    time.sleep(gwtests.iocRunDuration)
    iocControl.stop()
