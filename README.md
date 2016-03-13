# Channel Access PV Gateway

The Gateway is both a Channel Access server and Channel Access client.
It provides a means for many clients to access a process variable,
while making only one connection to the server that owns the process variable.

It also provides additional access security beyond that on the server.
It thus protects critical servers while providing possibly restricted access
to needed process variables.

The Gateway typically runs on a machine with multiple network cards,
and the clients and the server may be on different subnets.

## Continuous Integration

The [CA Gateway CI](https://openepics.ci.cloudbees.com/job/CA_Gateway/)
is hosted on [CloudBees](https://www.cloudbees.com/).

## Links

More details are available on the
[CA Gateway main web page](http://www.aps.anl.gov/epics/extensions/gateway/).
