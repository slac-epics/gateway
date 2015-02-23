#!/usr/bin/env python
import os
import unittest
import epics
import SIOCControl
import GatewayControl
import gwtests
import time

class DBEValueTest(unittest.TestCase):
    '''A "hello world" test. We start a IOC, gateway and then set up a monitor and make sure we receive the appropriate number of events.
    1) Establish a DBE_VALUE monitor on an ai - caput 10 changes; get 10 monitor events
    '''

    def setUp(self):
        self.siocControl = SIOCControl.SIOCControl()
        self.gatewayControl = GatewayControl.GatewayControl()
        self.eventsReceived = 0
        self.siocControl.startSIOCWithDefaultDB("12782")
        self.gatewayControl.startGateway(os.environ['EPICS_CA_SERVER_PORT'], "12782")
        time.sleep(2)
        epics.ca.initialize_libca()

        
    def tearDown(self):
        time.sleep(1)
        epics.ca.finalize_libca()
        self.siocControl.stop()
        time.sleep(1)
        self.gatewayControl.stop()
        
    def onChange(self, pvname=None, **kws):
        print pvname, " changed to ", kws['value']
        self.eventsReceived = self.eventsReceived + 1
        
    def testDBEValue(self):
        '''Establish a DBE_VALUE monitor on an ai - caput 10 changes; get 10 monitor events.'''
        if gwtests.verbose:
                print "Running DBEValueTest.testDBEValue"
        pv = epics.PV("gateway:passive0", auto_monitor=epics.dbr.DBE_VALUE)
        pv.add_callback(self.onChange)
        time.sleep(1)
        pv.put(-1)
        time.sleep(5)
        # Reset events received
        self.eventsReceived = 0
        for val in range(0,10):
            pv.put(val)
            time.sleep(1)
        self.assertTrue(self.eventsReceived == 10, 'We should have received 10 events; instead we received ' + str(self.eventsReceived))
        