#!/usr/bin/env python

import TargetData
import Port

t1 = TargetData.TargetData()
t2 = TargetData.TargetData()

print "Target 1: " + t1.toString()


t1.setIP("192.168.1.1")
t2.setIP("10.10.10.10")


print "Target 1: " + t1.toString()


port1 = Port.Port(True, 25)
t1.addPort(port1)

print "Target 1: " + t1.toString()

serial = t1.serialize()

print "Target 1 serialization: " + serial

t2.unserialize(serial)

print "Target 2 after deserialize: " + t2.toString()
