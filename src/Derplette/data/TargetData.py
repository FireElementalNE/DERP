
import pickle
import OperatingSystem
import Port
import Coordinates
import Timestamp
import os, re


# This is a class to store the data about a target


class TargetData:

	def __init__(self):
	
		# The IP Address
		self.ip_addr = None

		# The hostname
		self.hostname = None

		# The operating system
		self.os = None

		# The open ports
		self.port_list = []

		# The coordinates
		self.coordinates = None
	
		# The timestamp
		self.timestamp = Timestamp.Timestamp()


	def setIP(self, ip):

		self.ip_addr = ip
	
	def setHostname(self, hostname):

		self.hostname = hostname

	def setOS(self, os):

		self.os = os

	def addPort(self, port):

		self.port_list.append(port)

	def addCoordinates(self, coords):

		self.coordinates = coords

	def isNewer(self, tdata):
		
		if tdata == None:
			return True

		if not tdata == None and self.timestamp.isNewer(tdata.timestamp):
			return True

		return False

	def toString(self):
			
		s = ""
		s += "IP ADDRESS: " + str(self.ip_addr) + "\n"
		s += "HOSTNAME: " + str(self.hostname) + "\n"
		if not self.os == None:
			s += "OS: " + self.os.toString() + "\n"
		if not self.port_list == None:	
			for x in self.port_list:
				s += "PORT: " + x.toString() + "\n"

		if not self.coordinates == None:
			s += "COORDINATES: " + self.coordinates.toString() + "\n"
		if not self.timestamp == None:		
			s += "TIMESTAMP: " + self.timestamp.toString()

		return s


	def serialize(self):

		return pickle.dumps(self)

	def unserialize(self, s):
	
		obj = pickle.loads(s)
		self.ip_addr = obj.ip_addr
		self.hostname = obj.hostname
		self.os = obj.os
		self.port_list = obj.port_list
		self.coordinates = obj.coordinates
		self.timestamp = obj.timestamp

	def serializeToFile(self, fname, directory="./"):

		f = open(directory + fname,'w')
		pickle.dump(self, f)

	def unserializeFromFile(self, fname, directory="./"):

		print directory + fname

		f = open(directory + fname, 'r')
		obj = pickle.load(f)
		self.ip_addr = obj.ip_addr
		self.hostname = obj.hostname
		self.os = obj.os
		self.port_list = obj.port_list
		self.coordinates = obj.coordinates
		self.timestamp = obj.timestamp

