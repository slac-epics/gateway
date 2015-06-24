#!/usr/bin/env python
import unittest
import sys
import argparse
import os
import subprocess
import platform
from tap import TAPTestRunner
import gwtests

def suite():
    suite = unittest.TestLoader().loadTestsFromNames(['DBEValueTest', 'DBELogTest', 'DBEAlarmTest', 'DBEPropTest', 'PropertyCacheTest'])
    return suite

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--verbose_gateway', action='store_true', help='Enable verbose logging for the gateway. Starts the gateway in debug mode')
    parser.add_argument('-t', '--tests', nargs='*', help='Specify the tests that need to be run.')
    args = parser.parse_args()
    gwtests.verbose = args.verbose
    gwtests.verboseGateway = args.verbose_gateway

    if 'EPICS_HOST_ARCH' in os.environ:
        gwtests.hostArch = os.environ['EPICS_HOST_ARCH']
    elif 'T_A' in os.environ:
        gwtests.hostArch = os.environ['T_A']
    else:
        print "Warning: EPICS_HOST_ARCH not set. Using default value of 'linux-x86_64'"
    if 'TOP' in os.environ:
        gwtests.gwLocation = os.path.join(os.environ['TOP'], '..')
    else:
        print "Warning: TOP not set. Using default value of '..'"

    gatewayExecutable = os.path.join(gwtests.gwLocation, 'bin', gwtests.hostArch, 'gateway')
    if not os.path.exists(gatewayExecutable):
        print "Cannot find the gateway executable to test", gatewayExecutable
        sys.exit(1)
    
    if gwtests.verbose:
        verb = 2
    else:
        verb = 1

    if args.tests:
        test_suite = unittest.TestLoader().loadTestsFromNames(args.tests)
    else:
        test_suite = suite()

    runner = TAPTestRunner(verbosity=verb)
    if 'HARNESS_ACTIVE' in os.environ:
        runner.set_stream(True)
    runner.run(test_suite)
