import pickle


class Coordinates:

	def __init__(self, latVal = None, longVal = None):

		self.latitude = latVal
		self.longitude = longVal
		
	def setLatitude(self, latitude):
	
		self.latitude = latitude

	def setLongitude(self, longitude):

		self.longitude = longitude


	def toString(self):

		s = ""
		s += "( " + str(self.latitude)
		s += " , " + str(self.longitude)
		s += " )"
		return s 

	def isEqual(self, other):

		if other == None:
			return False
		if self.longitude != other.longitude:
			return False
		if self.latitude != other.latitude:
			return False

		return True

	def serialize(self):
		
		return pickle.dumps(self)

	def unserialize(self, s):
		
		obj = pickle.loads(s)
		self.longitude = obj.longitude
		self.latitude = obj.latitude
