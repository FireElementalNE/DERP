#!/usr/bin/env python

import os, sys, time
from DerpletteDaemon import *

     
if __name__ == "__main__":
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon = DerpletteDaemon(DERPLETTE_PIDFILE)
			daemon.start()
			cat_cmd = "cat " + DERPLETTE_PIDFILE
			pid = os.system(cat_cmd)
			print "Derplette started on port " + DERPLETTE_PORT + " with pid " + pid 
		elif 'stop' == sys.argv[1]:
			kill_cmd = "kill `cat " + DERPLETTE_PIDFILE  + "`"
			os.system(kill_cmd)
			os.remove(DERPLETTE_PIDFILE)
			print "Derplette killed"
		elif 'generate-keys' == sys.argv[1]:
			keygen_cmd = "ssh-keygen -t rsa -f " + DERPLETTE_RSA_PATH + " -q -N " + DERPLETTE_RSA_PASSPHRASE
			os.system(keygen_cmd)
			print "Derplette RSA keys created"
		elif 'register' == sys.argv[1]:
			d = Derplette()
			d.sendRegister()
		elif 'unregister' == sys.argv[1]:
			d = Derplette()
			d.sendUnregister()
		elif 'get-peers' == sys.argv[1]:
			d = Derplette()
			d.sendGetPeers()
		else:	
			print "Unknown command"
			sys.exit(2)
			sys.exit(0)
	else:
		print "usage: %s start|stop|generate-keys|register|unregister" % sys.argv[0]
		sys.exit(2)

