import pickle
import datetime
import time

class Timestamp:

	def __init__(self):

		self.timestamp = time.time()

	def stamp(self):

		self.timestamp = time.time()

	def getTimestamp(self):
	
		return self.timestamp

	def isNewer(self, other):

		if other == None:
			return True

		if self.timestamp > other.timestamp:
			return True

		return False

	def isEqual(self, other):
		
		if other == None:
			return False

		if self.timestamp == other.timestamp:
			return True

		return False

	def getUtcTime(self):

		return datetime.datetime.utcfromtimestamp(self.timestamp)

	def toString(self):

		return str(datetime.datetime.utcfromtimestamp(self.timestamp))


	# Create a serialized version of the object that can be used to recreate the object
	def serialize(self):

		return pickle.dumps(self)

	# Create an object from the serialized object
	def unserialize(self, s):

		obj = pickle.loads(s)
		self.timestamp = obj.getTimestamp()

