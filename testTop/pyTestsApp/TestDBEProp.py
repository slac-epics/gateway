#!/usr/bin/env python
import os
import unittest
import epics
import IOCControl
import GatewayControl
import gwtests
import time

class TestDBEProp(unittest.TestCase):
    '''Test property updates (client using DBE_PROPERTY flag) through the Gateway'''

    def setUp(self):
        gwtests.setup()
        self.iocControl = IOCControl.IOCControl()
        self.gatewayControl = GatewayControl.GatewayControl()
        self.iocControl.startIOC()
        self.gatewayControl.startGateway()
        os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
        os.environ["EPICS_CA_ADDR_LIST"] = "localhost:{0} localhost:{1}".format(gwtests.iocPort,gwtests.gwPort)
        epics.ca.initialize_libca()
        self.eventsReceived = 0

    def tearDown(self):
        epics.ca.finalize_libca()
        self.gatewayControl.stop()
        self.iocControl.stop()
        
    def onChange(self, pvname=None, **kws):
        self.eventsReceived += 1
        if gwtests.verbose:
            print pvname, " changed to ", kws['value']
        
    def testPropAlarmLevels(self):
        '''DBE_PROPERTY monitor on an ai - value changes generate no events; property changes generate events.'''
        # gateway:passive0 is a blank ai record
        ioc = epics.PV("ioc:passive0", auto_monitor=epics.dbr.DBE_PROPERTY)
        gw = epics.PV("gateway:passive0", auto_monitor=epics.dbr.DBE_PROPERTY)
        gw.add_callback(self.onChange)
        pvhihi = epics.PV("ioc:passive0.HIHI", auto_monitor=None)
        pvlolo = epics.PV("ioc:passive0.LOLO", auto_monitor=None)
        pvhigh = epics.PV("ioc:passive0.HIGH", auto_monitor=None)
        pvlow  = epics.PV("ioc:passive0.LOW",  auto_monitor=None)
        ioc.get()
        gw.get()

        for val in range(10):
            ioc.put(val, wait=True)
        time.sleep(.05)
        # We get 1 event: at connection
        self.assertTrue(self.eventsReceived == 1, 'events expected: 1; events received: ' + str(self.eventsReceived))

        self.eventsReceived = 0
        pvhihi.put(20.0, wait=True)
        pvhigh.put(18.0, wait=True)
        pvlolo.put(10.0, wait=True)
        pvlow.put(12.0, wait=True)
        time.sleep(.05)

        # We get 4 events: properties of four alarm levels changed
        self.assertTrue(self.eventsReceived == 4, 'events expected: 4; events received: ' + str(self.eventsReceived))


if __name__ == '__main__':
    unittest.main(verbosity=2)
