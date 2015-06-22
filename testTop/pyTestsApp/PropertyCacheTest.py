#!/usr/bin/env python
import os
import unittest
import epics
from epics import ca
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
        ca.initialize_libca()

    def tearDown(self):
        ca.finalize_libca()
        self.siocControl.stop()
        self.gatewayControl.stop()
        
    def onChange(self, pvname=None, **kws):
        a = 1

    def testPropCache_ValueMonitorFullPV(self):
        '''Monitor PV (value events) through GW - change HIGH directly - get the DBR_CTRL of the PV through GW'''
        # gwcachetest is an ai record with full set of alarm limits: -100 -10 10 100
        gw = ca.create_channel("gateway:gwcachetest")
        connected = ca.connect_channel(gw, timeout=.5)
        self.assertTrue(connected, "Could not connect to gateway channel " + ca.name(gw))
        (gw_cbref, gw_uaref, gw_eventid) = ca.create_subscription(gw, mask=epics.dbr.DBE_VALUE, callback=self.onChange)
        ioc = ca.create_channel("ioc:gwcachetest")
        connected = ca.connect_channel(ioc, timeout=.5)
        self.assertTrue(connected, "Could not connect to ioc channel " + ca.name(gw))
        (ioc_cbref, ioc_uaref, ioc_eventid) = ca.create_subscription(ioc, mask=epics.dbr.DBE_VALUE, callback=self.onChange)

        # limit should not have been updated
        ioc_ctrl = ca.get_ctrlvars(ioc)
        highVal = ioc_ctrl['upper_warning_limit']
        self.assertTrue(highVal == 10.0, "Expected IOC warning_limit: 10; actual limit: "+ str(highVal))
        gw_ctrl = ca.get_ctrlvars(gw)
        highVal = gw_ctrl['upper_warning_limit']
        self.assertTrue(highVal == 10.0, "Expected GW warning_limit: 10; actual limit: "+ str(highVal))

        epics.caput("ioc:gwcachetest.HIGH", 20, wait=True)

        # now the limit should have been updated
        ioc_ctrl = ca.get_ctrlvars(ioc)
        highVal = ioc_ctrl['upper_warning_limit']
        self.assertTrue(highVal == 20.0, "Expected IOC warning_limit: 20; actual limit: "+ str(highVal))
        gw_ctrl = ca.get_ctrlvars(gw)
        highVal = gw_ctrl['upper_warning_limit']
        self.assertTrue(highVal == 20.0, "Expected GW warning_limit: 20; actual limit: "+ str(highVal))
