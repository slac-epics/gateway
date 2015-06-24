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

    if 'EPICS_HOST_ARCH' not in os.environ or 'TOP' not in os.environ:
        print "Please set the EPICS_HOST_ARCH and TOP environment variables."
        sys.exit(1)

    gwtests.gwLocation = os.path.join(os.environ['TOP'], '..')
    gatewayExecutable = os.path.join(gwtests.gwLocation, 'bin', os.environ['EPICS_HOST_ARCH'], 'gateway')
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
