


# MAX MESSAGE LENGTH
MSG_MAX_LEN = 4096

# SEPARATORS
PEER_DATA_SEPARATOR = '#'
MESSAGE_DATA_SEPARATOR = ':'

# TYPES of MESSAGES
MSG_REGISTER = 			"REGISTER"
MSG_UNREGISTER = 		"UNRGSTER"
MSG_GET_PEERS = 		"GETPEERS"
MSG_REPORT_SCAN = 		"REPTSCAN"
MSG_GET_SCANS = 		"GETSCANS"
MSG_GET_PUBKEY = 		"GETPBKEY"
MSG_GET_LAST_UPDATE_PEER = 	"GETLSTUP"
MSG_GET_UPDATE = 		"GETUDATE"
MSG_TARGET_DATA =		"TRGTDATA"

class MessageData:

	def __init__(self, message_type, data, msg=None):
		if msg == None:
			self.message_type = message_type
			self.message_data = data
		else:
			msgtuple = msg.partition(MESSAGE_DATA_SEPARATOR)
			self.message_type = msgtuple[0]
			self.message_data = msgtuple[2]
	
	def toString(self):
		return self.message_type + MESSAGE_DATA_SEPARATOR + self.message_data

	def getMessageType(self):
		return self.message_type

	def getMessageData(self):
		return self.message_data

	def equals(self, m2):
		if self.message_type == m2.message_type and self.message_data == m2.message_data:
			return 2
	
		return 0

class PeerData:

	def __init__(self, host, port, msg=None):
		
		if msg == None:
			self.host = host
			self.port = port
		else:
			peertuple = msg.partition(PEER_DATA_SEPARATOR)
			self.host = peertuple[0]
			self.port = peertuple[2]
		
	def equals(self, p2):
		if self.host == p2.host and self.port == p2.port:
			return 1
		return 0
	

	def toString(self):
		return self.host + PEER_DATA_SEPARATOR + self.port


	def getPort(self):
		return self.port	

	def getHost(self):
		return self.host


