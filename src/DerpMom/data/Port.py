import pickle

class Port:

	def __init__(self, oVal, nVal=None, service=None):

		self.opened = oVal
		self.number = nVal
		self.service = service

	def addService(self, service):
	
		self.service = service



	def setNumber(self, nVal):

		self.number = nVal

	def getPortState(self):

		return self.opened

	def getPortNumber(self):
	
		return self.number

	def getService(self):

		return self.service

	def toString(self):

		s = ""
		s += "Port " + str(self.number) 
		s += ", " 
		if self.opened == "open":
			s += "opened"
		elif self.opened == "filtered":
			s += "filtered"
		else:
			s += "closed"
		if self.service != None:
			s += "Service: "
			s += self.service.toString()
		return s

	def isEqual(self, other):

		if other == None:
			return False
		if self.opened != other.opened:
			return False
		if self.number != other.number:
			return False
		if self.service == None and other.service != None:
			return False
		if self.service != None and other.service == None:		
			return False
		if self.service != None and other.service != None:	
			if not self.service.isEqual(other):
				return False

		return True


	def serialize(self):

		return pickle.dumps(self)


	def unserialize(self, s):

		obj = pickle.loads(s)
		self.opened = obj.opened
		self.number = obj.number
		self.service = obj.service


