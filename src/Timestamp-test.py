#!/usr/bin/env python

import Timestamp


# TEST 1: Create Timestamp
t1 = Timestamp.Timestamp()


print "Created a Timestamp."
print t1.toString() + "\n"

# TEST 1.5: Create a Second Timestamp
t2 = Timestamp.Timestamp()

print "Created a Timestamp"
print t2.toString() + "\n"


# TEST 2: Check to see if the first is newer should be false
val = t1.isNewer(t2)
print "Is the first timestamp newer, should be false: " + str(val) + "\n"


# TEST 3: Restamp the first timestamp
#          Then test
t1.stamp()

print "The new stamp is: " + t1.toString()
val2 = t1.isNewer(t2)
print "Is the restamped first timestamp newer, should be true: " + str(val2) + "\n" 

# TEST 4: Serialize the first timestamp
serial_string = t1.serialize()
print "The serialized string is: " + serial_string

# Test 5: Unserialize a string

t3 = Timestamp.Timestamp()
print "T3 is initialized as: " + t3.toString()
valEq1 = t1.isEqual(t3)
print "T1 and T3 equal? should be False: " + str(valEq1)
t3.unserialize(serial_string)
print "T3 is set to the serialized object: " + t3.toString()
valEq = t1.isEqual(t3)
print "T1 and T3 equal? Should be True: " + str(valEq)
