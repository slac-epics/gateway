#!/usr/bin/env python
'''Starts/stops the SIOC used in the tests'''
import os
import subprocess
import time
import gwtests

class SIOCControl:
    siocProcess = None
    DEVNULL = None

    def startSIOCWithDefaultDB(self):
        '''Start the SIOC using the default test.db'''
        childEnviron = os.environ.copy()
        childEnviron['EPICS_CA_SERVER_PORT'] = str(gwtests.iocPort)
        childEnviron['EPICS_CA_ADDR_LIST'] = "localhost"
        childEnviron['EPICS_CA_AUTO_ADDR_LIST'] = "NO"
        if not gwtests.verbose:
            self.DEVNULL = open(os.devnull, 'wb')
        self.siocProcess = subprocess.Popen(['softIoc', '-d', 'test.db'], env=childEnviron, stdout=self.DEVNULL, stderr=subprocess.STDOUT)
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
