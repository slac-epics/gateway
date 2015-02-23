#!/usr/bin/env python
'''Starts/stops the SIOC used in the tests'''
import os
import subprocess
import time

class SIOCControl:
    siocProcess = None

    def startSIOCWithDefaultDB(self, iocPort):
        '''Starts the SIOC using the default test.db'''
        childEnviron = os.environ.copy()
        childEnviron['EPICS_CA_SERVER_PORT'] = iocPort
        childEnviron['EPICS_CA_ADDR_LIST'] = "localhost"
        self.siocProcess = subprocess.Popen(['softIoc', '-d', 'test.db'], env=childEnviron)

    def stop(self):
        self.siocProcess.terminate()


if __name__ == "__main__":
    siocControl = SIOCControl()
    siocControl.startSIOCWithDefaultDB('12782')
    time.sleep(60)
    siocControl.stop()
