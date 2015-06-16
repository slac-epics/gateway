#!/usr/bin/env python
import os
import unittest
import epics
import SIOCControl
import GatewayControl
import gwtests
import time

class DBELogTest(unittest.TestCase):
    '''2) Establish DBE_LOG monitor on an ai with an ADEL - caput changes of which only 2 should be more than the ADEL ; get 2 monitor events. '''

    def setUp(self):
        self.siocControl = SIOCControl.SIOCControl()
        self.gatewayControl = GatewayControl.GatewayControl()
        self.eventsReceived = 0
        self.siocControl.startSIOCWithDefaultDB("12782")
        self.gatewayControl.startGateway(os.environ['EPICS_CA_SERVER_PORT'] if 'EPICS_CA_SERVER_PORT' in os.environ else "5064", "12782")
        time.sleep(2)
        os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
        os.environ["EPICS_CA_ADDR_LIST"] = "localhost"
        epics.ca.initialize_libca()

        
    def tearDown(self):
        time.sleep(1)
        epics.ca.finalize_libca()
        self.siocControl.stop()
        time.sleep(1)
        self.gatewayControl.stop()
        
    def onChange(self, pvname=None, **kws):
        if gwtests.verbose:
            print pvname, " changed to ", kws['value']
        self.eventsReceived = self.eventsReceived + 1
        
    def testDBELog(self):
        '''Establish DBE_LOG monitor on an ai with an ADEL - caput changes of which only 2 should be more than the ADEL ; get 2 monitor events.'''
        print "Running DBELogTest.testDBELog"
        pv = epics.PV("gateway:passiveADEL", auto_monitor=epics.dbr.DBE_LOG)
        pv.add_callback(self.onChange)
        time.sleep(1)
        pv.put(-1)
        time.sleep(5)
        # Reset events received
        self.eventsReceived = 0
        
        for val in range(1,30,2):
            pv.put(val)
            time.sleep(1)
        self.assertTrue(self.eventsReceived == 2, 'We should have received 2 events; instead we received ' + str(self.eventsReceived))
        
