#!/usr/bin/env python
import os
import unittest
import epics
import SIOCControl
import GatewayControl
import gwtests
import time
import subprocess

class PropertyCacheTest(unittest.TestCase):
    '''The gateway caches the properties; we want it to establish a DBE_PROP monitor no matter what and update its internal property cache
    Establish no monitors - make a change to the HIGH outside of the gateway; then ca_get the value of the PV's HIGH from the gateway; received changed value
    '''

    def setUp(self):
        self.siocControl = SIOCControl.SIOCControl()
        self.gatewayControl = GatewayControl.GatewayControl()
        self.siocControl.startSIOCWithDefaultDB()
        self.gatewayControl.startGateway()
        os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
        os.environ["EPICS_CA_ADDR_LIST"] = "localhost:{} localhost:{}".format(gwtests.iocPort,gwtests.gwPort)
        epics.ca.initialize_libca()

    def tearDown(self):
        epics.ca.finalize_libca()
        self.siocControl.stop()
        self.gatewayControl.stop()
        
    def onChange(self, gwname=None, **kws):
        a = 1

    def testPropCache_ValueMonitorFullPV(self):
        '''Monitor PV (value events) through GW - change HIGH directly - get the DBR_CTRL of the PV through GW'''
        # gwcachetest is an ai record with full set of alarm limits: -100 -10 10 100
        gw = epics.PV("gateway:gwcachetest", form='ctrl', auto_monitor=epics.dbr.DBE_VALUE)
        gw.add_callback(self.onChange)
        ioc = epics.PV("ioc:gwcachetest", form='ctrl', auto_monitor=epics.dbr.DBE_VALUE)
        ioc.add_callback(self.onChange)

        epics.caput("ioc:gwcachetest.HIGH", 20, wait=True)

        # limit should not have been updated (value monitor)
        highVal = ioc.upper_warning_limit
        self.assertTrue(highVal == 10.0, "Expected IOC warning_limit: 10; actual limit: "+ str(highVal))
        highVal = gw.upper_warning_limit
        self.assertTrue(highVal == 10.0, "Expected GW warning_limit: 10; actual limit: "+ str(highVal))
        # do an explicit get
        gw.get(use_monitor=False)
        ioc.get(use_monitor=False)
        # now the limit should have been updated
        highVal = ioc.upper_warning_limit
        self.assertTrue(highVal == 20.0, "Expected IOC warning_limit: 20; actual limit: "+ str(highVal))
        highVal = gw.upper_warning_limit
        self.assertTrue(highVal == 20.0, "Expected GW warning_limit: 20; actual limit: "+ str(highVal))
