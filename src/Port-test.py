#!/usr/bin/env python

import Port

# TEST 1: Create an empty port
emptyPort = Port.Port()
print "The empty port to string: " + emptyPort.toString()

# TEST 2: Create an opened port with a number
port2 = Port.Port(True, 25)
print "The non-empty port to string: " + port2.toString()

# TEST 3: 
serial_string1 = emptyPort.serialize()
print "The serialized port1: " + serial_string1

# TEST 4: 
serial_string2 = port2.serialize()
print "The serialized port2: " + serial_string2

# Test 5"
rVal = emptyPort.isEqual(port2)
print "Test if ports are equal, should be False: " + str(rVal)

# Test 6"
port2.unserialize(serial_string1)
print "Port2 has been made from port1 serial string: " + port2.toString()

# Test 7"
print "Are the ports now equal, should be True: " + str(emptyPort.isEqual(port2))
