#!/usr/bin/env python

import Coordinates

# TEst 1 make some coordingates
c1 = Coordinates.Coordinates(10, 20)
print "Coordinates1: " + c1.toString()

# Test 2 make some coordinates
c2 = Coordinates.Coordinates(20, 40)
print "Coordingates2: " + c2.toString()

# Test equality
eqVal = c1.isEqual(c2)
print "Test equality, should be False: " + str(eqVal)

# Test 4: serialize c1
serial = c1.serialize()
print "C1 serial: " + serial

# Test 5 : unserialize c2 from c1serial
c2.unserialize(serial)
print "C2 made from C1 serial: " + c2.toString()

# Test 6: check equality again
eqVal = c1.isEqual(c2)
print "Test equality, should be True: " + str(eqVal)
