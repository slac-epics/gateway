#!/usr/bin/env python
import os
import unittest
import epics
import SIOCControl
import GatewayControl
import gwtests
import time

class DBEPropTest(unittest.TestCase):
    '''Establish DBE_PROPERTY monitor on an ai - caput 10 changes; get 0 monitor events; caput on the HIHI; get 1 monitor event'''

    def setUp(self):
        self.siocControl = SIOCControl.SIOCControl()
        self.gatewayControl = GatewayControl.GatewayControl()
        self.eventsReceived = 0
        self.siocControl.startSIOCWithDefaultDB("12782")
        self.gatewayControl.startGateway(os.environ['EPICS_CA_SERVER_PORT'] if 'EPICS_CA_SERVER_PORT' in os.environ else "5064", "12782")
        time.sleep(2)
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
        
    def testDBEProp(self):
        '''Establish DBE_PROPERTY monitor on an ai - caput 10 changes; get 0 monitor events; caput on the HIHI; get 1 monitor event'''
        if gwtests.verbose:
                print "Running DBEPropTest.testDBEProp"
        pv = epics.PV("gateway:passive0", auto_monitor=epics.dbr.DBE_PROPERTY)
        pv.add_callback(self.onChange)
        pvhihi = epics.PV("gateway:passive0.HIHI", auto_monitor=None)
        time.sleep(1)
        for val in range(0,10):
            pv.put(val)
            time.sleep(1)
        self.assertTrue(self.eventsReceived == 1, 'We should have received only the initial event; instead we received ' + str(self.eventsReceived))
        pvhihi.put(20.0)
        time.sleep(1)
        self.assertTrue(self.eventsReceived == 2, 'We should have received an additional event for the property change ' + str(self.eventsReceived))
        
