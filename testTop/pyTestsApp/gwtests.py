#!/usr/bin/env python

# Do we want verbose logging
verbose = False
# Do we want debug logging from the gateway
verboseGateway = False

# CA ports to use
iocPort = 12782
gwPort = 12783

# Duration of standalong runs
gwRunDuration = 300
iocRunDuration = 300

# Gateway attributes
gwStatsPrefix = "gwtest"

# Defaults for EPICS properties:
gwLocation = "../.."
hostArch = "linux-x86_64"
