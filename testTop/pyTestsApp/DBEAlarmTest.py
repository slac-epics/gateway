#!/usr/bin/env python
import os
import unittest
import epics
import SIOCControl
import GatewayControl
import gwtests
import time

class DBEAlarmTest(unittest.TestCase):
    '''3) Establish DBE_ALARM monitor on an ai with an ADEL - caput changes of which none are more than the ADEL; however, few changes generates alarm changes'''

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
        ''' Establish DBE_ALARM monitor on an ai with an ADEL - caput changes of which none are more than the ADEL; however, few changes generates alarm changes'''
        print "Running DBEAlarmTest.testDBELog"
        pv = epics.PV("gateway:passiveALRM", auto_monitor=epics.dbr.DBE_ALARM)
        pv.add_callback(self.onChange)
        time.sleep(1)
        for val in [0,1,2,3,4,5,6,5,4,3,2,1,0]:
            pv.put(val)
            time.sleep(1)
        # We actually get 4 events as the value crosses the alarm three times; once during the initial set to 0. 
        self.assertTrue(self.eventsReceived == 4, 'We should have received 4 events; instead we received ' + str(self.eventsReceived))
        
