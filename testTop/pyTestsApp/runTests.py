#!/usr/bin/env python
import unittest
import sys
import argparse
import os
import subprocess
import platform
import gwtests

def suite():
    suite = unittest.TestLoader().loadTestsFromNames(['DBEValueTest', 'DBELogTest', 'DBEAlarmTest', 'DBEPropTest', 'GatewayPropCacheTest'])
    return suite

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('-t', '--tests', help='Specify the tests that need to be run.')
    args = parser.parse_args()
    gwtests.verbose = args.verbose
    
    
    if args.tests:
        runner = unittest.TextTestRunner()
        test_suite = unittest.TestLoader().loadTestsFromNames([args.tests])
        runner.run (test_suite)
    else:
        runner = unittest.TextTestRunner()
        test_suite = suite()
        runner.run (test_suite)
