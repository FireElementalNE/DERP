import pickle

class OperatingSystem:

	def __init__(self, osName=None, vName=None, majNum=None, minNum=None):

		self.os_name = osName
		self.version_name = vName
		self.major_number = majNum
		self.minor_number = minNum

	def isEqual(self, other):

		if other == None:
			return False
		if self.os_name != other.os_name:
			return False
		if self.version_name != other.version_name:
			return False
		if self.major_number != other.major_number:
			return False
		if self.minor_number != other.minor_number:
			return False
		
		return True

	def toString(self):

		s = ""
		if self.os_name != None:
			s += self.os_name
		if self.version_name != None:
			if len(s) > 0:
				s += " "
			s += self.version_name
		if self.major_number != None:
			s += " "
			s += self.major_number
		if self.minor_number != None:
			s += " "
			s += self.minor_number
		return s

	def serialize(self):

		return pickle.dumps(self)


	def unserialize(self, s):
	
		obj = pickle.loads(s)
		self.os_name = obj.os_name
		self.version_name = obj.version_name
		self.major_number = obj.major_number
		self.minor_number = obj.minor_number
