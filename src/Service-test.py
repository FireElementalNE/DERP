#!/usr/bin/env python

import Service


s1 = Service.Service()
s2 = Service.Service("Apache 2.0")


print "Service 1 toString(): " + s1.toString()
print "Service 2 toString(): " + s2.toString()

s1serial = s1.serialize()
s2serial = s2.serialize()

print "Service 1 serial: " + s1serial
print "Service 2 serial: " + s2serial

eqVal = s1.isEqual(s2)
print "Are they equal, should be false: " + str(eqVal)

s2.unserialize(s1serial)
print "S2 ffrom S1 serial: " + s2.toString()

eqVal = s1.isEqual(s2)
print "Are they equal now, should be true: " + str(eqVal)

