#!/usr/bin/env python

# This file represents the Derplette

# Import sockets
import socket
import os, sys

# Import the peer-2-peer messaging protocol
from data.P2P_MSG import *

# Import from the Derplette Configuration
from DERPLETTE_CONFIG import *

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST,PORT))

#p = PeerData("127.0.0.1",str(40000))
#msg = MessageData("REGISTER",p.toString())

#regmsg = msg.toString()
#data = s.recv(1024)
#s.close()
#print 'Received', repr(data)

import data.TargetData

class Derplette:

	def __init__(self):

		# This class stores a port number
		self.port = DERPLETTE_PORT_NUM

		# This also store a host
		self.host = DERPLETTE_HOST

		# This class also storesa socket
		self.serv = None

		# The public and private keys
		self.pubkeypath = DERPLETTE_RSA_PATH + ".pub"
		self.privkeypath = DERPLETTE_RSA_PATH


	def initSocket(self):
	
		for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
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

	# --------------------------------------------------
	# Get a connection
	# --------------------------------------------------
	def getConnection(self):

		# get the connection properties
		conn, addr = self.serv.accept()
		while 1:
			data = self.processMessage(conn.recv(MSG_MAX_LEN))
			if not data: break
			conn.send(data)
		conn.close()

	# --------------------------------------------------
	# Process a Message
	# --------------------------------------------------
	def processMessage(self, msg):

		# Get the message data from the message
		msg_data = MessageData(None, None, msg)
		message_data = msg_data.getMessageData()

		if msg_data.getMessageType() == MSG_TARGET_DATA:

			serial = msg_data.getMessageData()
			tdata = TargetData.TargetData()
			tdata.unserialize(serial)
			tdata.serializeToFile(tdata.ip_addr,TARGET_DATA_DIR)

			return "Thanks"
		else:
			if DEBUG:
				print "received unknown"

		# Return the message
		return msg

	def sendRegister(self):

		skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		skt.connect((DERPLETTE_DERPMOM_HOST, DERPLETTE_DERPMOM_PORT))
		derplette_data = PeerData(DERPLETTE_HOST,str(DERPLETTE_PORT_NUM))
		msg = MessageData(MSG_REGISTER, derplette_data.toString())
		regmsg = msg.toString()
		skt.send(regmsg)
		data = skt.recv(MSG_MAX_LEN)
		skt.close()
		print 'Received', repr(data)

	def sendUnregister(self):

                skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                skt.connect((DERPLETTE_DERPMOM_HOST, DERPLETTE_DERPMOM_PORT))
                derplette_data = PeerData(DERPLETTE_HOST,str(DERPLETTE_PORT_NUM))
                msg = MessageData(MSG_UNREGISTER, derplette_data.toString())
                regmsg = msg.toString()
                skt.send(regmsg)
		data = skt.recv(MSG_MAX_LEN)
                skt.close()
		print 'Received', repr(data)

	def sendTargetData(self, targetData):

		skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		skt.connect((DERPLETTE_DERPMOM_HOST, DERPLETTE_DERPMOM_PORT))
		msg = MessageData(MSG_TARGET_DATA, targetData.serialize())
		tdatamsg = msg.toString()
		skt.send(tdatamsg)
		data = skt.recv(MSG_MAX_LEN)
		skt.close()
		print 'Received', repr(data)

		retval = os.fork()

		if retval == 0:

			# Update all of the peers
			peers = self.sendGetPeers().split('\n')
		
			for peer in peers:
				if peer != '':
					host, port = peer.split()
					print "host: " + str(host)
					print "port: " + str(port)				

					if not host == DERPLETTE_HOST or not port == DERPLETTE_PORT_NUM:
						skt2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
						skt2.connect((host,int(port)))
						skt2.send(tdatamsg)
						ack = skt2.recv(MSG_MAX_LEN)
						skt2.close()

			sys.exit()

	def sendGetPeers(self):

		skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		skt.connect((DERPLETTE_DERPMOM_HOST, DERPLETTE_DERPMOM_PORT))
		msg = MessageData(MSG_GET_PEERS, "")
		regmsg = msg.toString()
		skt.send(regmsg)
		data = skt.recv(MSG_MAX_LEN)
		return data
