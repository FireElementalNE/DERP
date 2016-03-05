#!/usr/bin/env python

import OperatingSystem

# Test 1: Create an OS
os1 = OperatingSystem.OperatingSystem()
print "OS1: " + os1.toString()

# Test 2: Create a second OS
os2 = OperatingSystem.OperatingSystem("Ubuntu","Karmic Koala", "11", "04")
print "OS2: " + os2.toString()

# Test 3: Test the equality
eqVal = os1.isEqual(os2)
print "OSes equal, should be False: " + str(eqVal)

# Test 4: Serialize OS1
serial = os1.serialize()
print "Serialized OS1: " + serial

# Test 5: Load Os1 serial to OS2
os2.unserialize(serial)
print "OS2 unserialized OS1: " + os2.toString()

# Test 6: Check equality again
eqVal = os1.isEqual(os2)
print "OSes equal, should be True: " + str(eqVal)
