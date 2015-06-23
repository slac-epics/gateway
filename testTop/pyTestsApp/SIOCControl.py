#!/usr/bin/env python
'''Starts/stops the IOC used in the tests'''
import os
import subprocess
import time
import gwtests

class SIOCControl:
    siocProcess = None
    DEVNULL = None

    def startSIOCWithDefaultDB(self):
        '''Start the IOC using the default test.db'''
        childEnviron = os.environ.copy()
        childEnviron['EPICS_CA_SERVER_PORT'] = str(gwtests.iocPort)
        childEnviron['EPICS_CA_ADDR_LIST'] = "localhost"
        childEnviron['EPICS_CA_AUTO_ADDR_LIST'] = "NO"
        if not gwtests.verbose:
            self.DEVNULL = open(os.devnull, 'wb')

        siocExe = 'softIoc'
        if 'EPICS_BASE' in os.environ:
            if 'EPICS_HOST_ARCH' not in os.environ:
                print "Please set the EPICS_HOST_ARCH environment variable to the appropriate value."
                sys.exit(1)
            siocExe = "{0}/bin/{1}/softIoc".format(os.environ['EPICS_BASE'],os.environ['EPICS_HOST_ARCH'])
        siocCommand = [siocExe, '-d', 'test.db']

        if gwtests.verbose:
            print "Starting the IOC using\n", " ".join(siocCommand)
        self.siocProcess = subprocess.Popen(siocCommand, env=childEnviron, stdout=self.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(.5)

    def stop(self):
        self.siocProcess.terminate()
        if self.DEVNULL:
            self.DEVNULL.close()


if __name__ == "__main__":
    siocControl = SIOCControl()
    siocControl.startSIOCWithDefaultDB()
    time.sleep(gwtests.iocRunDuration)
    siocControl.stop()
