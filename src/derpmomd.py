#!/usr/bin/env python

import os, sys, time
from DerpMomDaemon import *

     
if __name__ == "__main__":
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon = DerpMomDaemon(DERPMOM_PIDFILE)
			daemon.start()
			cat_cmd = "cat " + DERPMOM_PIDFILE
			pid = os.system(cat_cmd)
			print "DerpMom started on port " + DERPMOM_PORT + " with pid " + pid 
		elif 'stop' == sys.argv[1]:
			kill_cmd = "kill `cat " + DERPMOM_PIDFILE  + "`"
			os.system(kill_cmd)
			os.remove(DERPMOM_PIDFILE)
			print "DerpMom killed"
		elif 'generate-keys' == sys.argv[1]:
			keygen_cmd = "ssh-keygen -t rsa -f " + DERPMOM_RSA_PATH + " -q -N " + DERPMOM_RSA_PASSPHRASE
			os.system(keygen_cmd)
			print "DerpMom RSA keys created"
		else:
			print "Unknown command"
			sys.exit(2)
			sys.exit(0)
	else:
		print "usage: %s start|stop|generate-keys" % sys.argv[0]
		sys.exit(2)

