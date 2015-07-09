#!/usr/bin/env python
'''Controls the test IOC'''
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
        # IOC_ environment overrides
        for v in os.environ.keys():
            if v.startswith("IOC_"):
                childEnviron[v.replace("IOC_", "", 1)] = os.environ[v]

        if not gwtests.verbose:
            self.DEVNULL = open(os.devnull, 'wb')

        if 'IOC_EPICS_BASE' in os.environ:
            iocCommand = [gwtests.iocExecutable, '-D', os.path.join(os.environ['IOC_EPICS_BASE'], 'dbd', 'softIoc.dbd')]
        else:
            iocCommand = [gwtests.iocExecutable]

        if arglist is None:
            iocCommand.extend(['-d', 'test.db'])
        else:
            iocCommand.extend(arglist)

        if gwtests.verbose:
            print "Starting the IOC using\n", " ".join(iocCommand)
        self.iocProcess = subprocess.Popen(iocCommand, env=childEnviron,
                stdin=subprocess.PIPE, stdout=self.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(.5)

    def stop(self):
        '''Stops the test IOC'''
        self.iocProcess.stdin.close()
        if self.DEVNULL:
            self.DEVNULL.close()


if __name__ == "__main__":
    gwtests.setup()
    print "Running the test IOC in verbose mode for {0} seconds".format(gwtests.gwRunDuration)
    gwtests.verbose = True
    iocControl = IOCControl()
    iocControl.startIOC()
    time.sleep(gwtests.iocRunDuration)
    iocControl.stop()
