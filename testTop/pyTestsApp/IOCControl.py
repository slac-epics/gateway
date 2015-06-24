#!/usr/bin/env python
'''Starts/stops the IOC used in the tests'''
import os
import subprocess
import time
import gwtests

class IOCControl:
    iocProcess = None
    DEVNULL = None

    def startIOC(self, arglist=None):
        '''Start the IOC using the default test.db'''
        childEnviron = os.environ.copy()
        childEnviron['EPICS_CA_SERVER_PORT'] = str(gwtests.iocPort)
        childEnviron['EPICS_CA_ADDR_LIST'] = "localhost"
        childEnviron['EPICS_CA_AUTO_ADDR_LIST'] = "NO"
        if not gwtests.verbose:
            self.DEVNULL = open(os.devnull, 'wb')

        iocExe = 'softIoc'
        if 'EPICS_BASE' in os.environ:
            iocExe = "{0}/bin/{1}/softIoc".format(os.environ['EPICS_BASE'],gwtests.hostArch)

        if arglist is None:
            iocCommand = [iocExe, '-d', 'test.db']
        else:
            iocCommand = [iocExe]
            iocCommand.extend(arglist)

        if gwtests.verbose:
            print "Starting the IOC using\n", " ".join(iocCommand)
        self.iocProcess = subprocess.Popen(iocCommand, env=childEnviron, stdout=self.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(.5)

    def stop(self):
        self.iocProcess.terminate()
        if self.DEVNULL:
            self.DEVNULL.close()


if __name__ == "__main__":
    iocControl = IOCControl()
    iocControl.startIOCWithDefaultDB()
    time.sleep(gwtests.iocRunDuration)
    iocControl.stop()
