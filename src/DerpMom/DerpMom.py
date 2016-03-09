#!/usr/bin/env python

# ---------------------------------------------------
# This server will support both ipv4 and ipv6
#
#
#
#
# ---------------------------------------------------
import socket
import sys

# import sets for the peer list
from sets import Set

# import the messaging protocol
from data.P2P_MSG import *

# import the tracker configuration
from DERPMOM_CONFIG import *

import data.TargetData

class DerpMom:
	
	# -----------------------------------------
	# The init function.
	# This should create the socket
	# ------------------------------------------
	def __init__(self):
			
		# This class stores a port number
		self.port = DERPMOM_PORT_NUM

		# This also store a host
		self.host = DERPMOM_HOST
		
		# This class also stores a socket that is a server
		self.serv = None
		
		# The public and private keys
		self.pubkeypath = DERPMOM_RSA_PATH + ".pub"
		self.privkeypath = DERPMOM_RSA_PATH 

		# This is a list of peers
		self.peer_list = Set([])

		# This is a list of scanned targets
		

	def initSocket(self):

		for res in socket.getaddrinfo(self.host , self.port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
			af, socktype, proto, canonname, sa = res
			try:
				self.serv = socket.socket(af, socktype, proto)
			except socket.error, msg:
				self.serv = None
				continue
			try:
				self.serv.bind(sa)
				self.serv.listen(1)
			except socket.error, msg:
				self.serv.close()
				self.serv = None
				continue
			break
		if self.serv is None:
			print 'could not open socket'
			sys.exit(1)
		
	
	# -------------------------------------------
	# Get a connection
	# -------------------------------------------
	def getConnection(self):

		# get the connection properties
		conn, addr = self.serv.accept()
		while 1:
			data = self.processMessage(conn.recv(MSG_MAX_LEN))
			if not data: break
			conn.send(data)
		conn.close()


	# -------------------------------------------
	# register a peer
	# -------------------------------------------
	def registerDerplette(self, pData):

		if pData.toString() in self.peer_list:
			if DEBUG:
				print "Peer already registered"
		else:
			self.peer_list.add(pData.toString())

	# -------------------------------------------
	# unregister a peer
	# -------------------------------------------
	def unregisterDerplette(self, pData):

		# pData is of type PeerDatai
		if pData.toString() in self.peer_list:
			self.peer_list.remove(pData.toString())
		else:
			if DEBUG:
				print "Peer not in list"
	# ------------------------------------------
	# get a peer list string
	# ------------------------------------------
	def getPeerListString(self):
		s = ""

		for x in range(0, len(self.peer_list)):
			s += str(PeerData(None, None, list(self.peer_list)[x] ).getHost())
			s += " "
			s += str(PeerData(None, None, list(self.peer_list)[x] ).getPort())
			s += "\n"

		return s

	# ------------------------------------------
	# print a peer list
	# ------------------------------------------
	def printPeerList(self): 
		print self.getPeerListString()

	# -------------------------------------------
	# process a message
	# -------------------------------------------
	def processMessage(self, msg):

		# Get the message data from the message
		msg_data = MessageData(None, None, msg)

		message_data = msg_data.getMessageData()


		# ---------- REGISTER A PEER ----------------

		if msg_data.getMessageType() == MSG_REGISTER:

			# print a debug message if debugging is enabled
			if DEBUG:
				 print "Received a Register"
	
			# Get a peerData object from the string
			pData = PeerData(None, None, message_data)

			# Register the Node using the PeerData object
			self.registerDerplette(pData)

		# ----------- UNREGISTER A PEER --------------

		elif msg_data.getMessageType() == MSG_UNREGISTER:

			# print a debug message if debugging is enabled
			if DEBUG:
				print "received a Unregister"

			# Get a peerData object from the string
			pData = PeerData(None, None, message_data)

			# Unregiseter the Node using the PeerData object
			self.unregisterDerplette(pData)

		# ------------ Get Target Data ----------------

		elif msg_data.getMessageType() == MSG_TARGET_DATA:

			serial = msg_data.getMessageData()
			tdata = data.TargetData.TargetData()
			tdata.unserialize(serial)
			tdata.serializeToFile(tdata.ip_addr,DERPMOM_TARGET_DATA_DIR)

		elif msg_data.getMessageType() == MSG_GET_PEERS:

			# print a debug message if debugging is enabled
			if DEBUG:
				print "received a Get Peers"
	
			return self.getPeerListString()

		elif msg_data.getMessageType() == MSG_REPORT_SCAN:

			# This is unimplemented
			lol =1
	

		elif msg_data.getMessageType() == MSG_GET_SCANS:

			# This is unimplemented
			lol =1

		elif msg_data.getMessageType() == MSG_GET_PUBKEY:

			# This is unimplemented
			lol =1

		elif msg_data.getMessageType() == MSG_GET_LAST_UPDATE_PEER:

			# This is unimplemented
			lol =1

		else:

			# print a debug message if debigging is enabled
			if DEBUG:
				print "received unknown"

		# Return the message
		return msg

