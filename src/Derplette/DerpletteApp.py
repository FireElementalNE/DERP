#--------------------------------------------------------------------------------
#
#                              Derp GUI in python TK
#
#--------------------------------------------------------------------------------

# For stuff involving TK
from Tkinter import *

from libs.pygmaps import maps
from pygeoip import GeoIP
import os
import sys
import re
import webbrowser
import errno
import socket
import subprocess
from time import gmtime, strftime
import threading

# Data Classes
import data.Coordinates
import data.Port
import data.Service
import data.TargetData
import data.Timestamp
import data.parseXML
import data.DirectoryViewerApp

import WorkerThread

# Derp class
import Derplette, DerpletteDaemon
from DERPLETTE_CONFIG import *

class DerpletteApp:
	# TODO: stop using os.system() use subprocess.popen()
	IP = '' #Next items are created for simple transfer of data
	hostName = ''
	ports = {}
	state = ''
	def __init__(self,root):
		"""
		creates TK object
		:param root: ???
		"""
        # TODO: lookup root
		frame = Frame(root)
		frame.pack()
	
		self.target_label = Label(frame, text="Target:")
		self.target_label.grid(row=0, column=0, columnspan=1)
        
		self.target = StringVar() #target box
		self.textbox = Entry(frame,textvariable=self.target)
		self.target.set("wikipedia.org")
		self.textbox.grid(row=0, column=1, columnspan=4)

		self.target_label = Label(frame, text="NMAP Args:")
		self.target_label.grid(row=1, column=0, columnspan=1)

		self.target = StringVar() #argument box
		self.textbox1 = Entry(frame,textvariable=self.target)
		self.target.set("-sV -p20")
		self.textbox1.grid(row=1, column=1, columnspan=4)
       
		self.scanButton = Button(frame, text='SCAN', command=self.scanit) #button to initiate scan of target
		self.scanButton.grid(row=2,column=0, columnspan=1)

		self.reg_button = Button(frame, text='Register', command=self.register)
		self.reg_button.grid(row=2, column=1, columnspan=1)

		self.unreg_button = Button(frame, text='Unregister', command=self.unregister)
		self.unreg_button.grid(row=2,column=2,columnspan=1)

		self.gen_button = Button(frame, text='GenKeys', command=self.generateKeys)
		self.gen_button.grid(row=2,column=3,columnspan=1)

		self.view_button = Button(frame, text='View', command=self.viewTargetData)
		self.view_button.grid(row=2,column=4,columnspan=1)

		self.button = Button(frame, text='Quit', command=root.destroy) #button to quit
		self.button.grid(row=2,column=5, columnspan=1)


	def build_target_data(self, target_ip, coord):
		"""
		takes the coordinates and the target_ip and creates a TargetData object
		:param target_ip: the ip of the target
		:param coord: a tuple of longitude and latitude
		:return: the target_data object built off of the two params
		"""
		xml_path =  TARGET_XML + target_ip + '.xml'
		temp_dict = {}
		run_time, host_name, host_ip, temp_dict = data.parseXML.parseMyXML(xml_path)
		# Create a target DATA 
		target_data = self.createTargetData(target_ip, temp_dict, host_name, coord[0], coord[1])		
		# Write the TargetData to a file
		target_data.serializeToFile(target_data.ip_addr, TARGET_DATA_DIR)
		return target_data

	def send_target_to_derpmom(self,target_data):
		"""
		sends TargetData object to the registered DerpMom
		:param target_data: the TargetData object of the target
		:return: nothing
		"""
		try:
			d = Derplette.Derplette()
			d.sendTargetData(target_data)
		except socket.error as e:
			if e.errno == errno.ECONNREFUSED:
				print "Could not connect to DerpMom...."

	def nmap_scan(self,target_ip, coord):
		"""
		creates an nmap scan of the target and sends out
		:param target_ip: the ip of the target
		:param coord: a tuple of longitude and latitude
		:return: nothing
		"""
		args = self.textbox1.get()
		if '-oX' in args:
			print 'ERROR: Cannot use -oX option (we already did that for you).'
		else:
			args += ' -oX ' + TARGET_XML + target_ip + '.xml'
			command = 'nmap ' + args + ' ' + target_ip + ' > /dev/null';
			print command
			p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			(out, err) = (p.stdout, p.stderr)
			# TODO: make this better
			if len(err.read()) < 5:
				target_data = self.build_target_data(target_ip, coord)
				self.send_target_to_derpmom(target_data)
			else:
				print 'Somthing went wrong with the scan:'
				print len(err.read())


	def scanit(self): #funtion to scan on record results
		"""
		scans a target, the target is taken from the TK box target
		:return: nothing
		"""
		gic = GeoIP(GEOIP_DATABASE) #change this to the location of GeoLiteCity.dat
		target = self.textbox.get()
		if target != '' and target != 'IP or Hostname': #error checking (not empty string)
			try:
				target_ip = socket.gethostbyname(target) #attempts to get an ip from hostnam/ip passed through 
				gic = GeoIP(GEOIP_DATABASE) #load geoIP database
				addr = gic.record_by_addr(target_ip) #if this works (getting ip) find address of ip
				lat = addr['latitude']
				lng = addr['longitude']
				htmlPath = TARGET_HTML + target_ip + '.html'
				mymap = maps(lat,lng,16) #create google map file
				mymap.addradpoint(lat, lng, 100, "#0000FF")
				mymap.draw(htmlPath)
				# TODO: maybe add this back later...
				# if lng != 0 and lat !=  0:
				#	webbrowser.open(htmlPath)
				self.nmap_scan(target_ip, [lat,lng])
			except socket.gaierror: #if finding IP fails
				print 'ERROR: Counld not get ip from hostname'
			except TypeError:  #if ip has no address (like 127.0.0.1) set lat and lng to 0,0
				# TODO: make more graceful
				print 'Could not get coordinates from GeoIP Database.'


	# -------------------------------------------------------------
	#  Create Target Data
	#
	#	This function takes an IP Address, NMAP PortScanner, 
	# 		and two coordinates and creates a TargetDataObject 
	# --------------------------------------------------------------
	def createTargetData(self, targetIP, tempDict, hostName, lat, lng):
		"""
		creates a target data object from the arguments
		:param targetIP: the ip of the target
		:param tempDict: ports
		:param hostName: the hostname of the target
		:param lat: the latitude of the target
		:param lng: the longitude of the target
		:return: a TargetData object
		"""
  
		# Create an empty Target Data object
		target_data = data.TargetData.TargetData()

		# Add the ip address and hostname
		target_data.setIP(str(targetIP))
		target_data.setHostname(hostName)

		# Create a coordinates object from the coordinates
		# 	and add it to the target data
		c = data.Coordinates.Coordinates(lat,lng)
		target_data.addCoordinates(c)
		
		# Create ports and add them to the target data
		for key,value in tempDict.iteritems():            		
			pNum = str(key)            
			pState = str(value[2])
			tempPort = data.Port.Port(pState,pNum)
			target_data.addPort(tempPort)
		
		# Return the created target data object 
		return target_data


	def register_threaded(self):
		daemon = DerpletteDaemon.DerpletteDaemon(DERPLETTE_PIDFILE)
		daemon.start()

	# -----------------------------------------------------------------
	#  Register
	# -----------------------------------------------------------------
	def register(self):
		"""
		uses a fork() syscall to create a daemon and registers with the derpmom
		:return: nothing
		"""
		retval = os.fork()
		if retval == 0:
			pool = WorkerThread.ThreadPool(1)
			pool.add_task(self.register_threaded)
			pool.wait_completion()
			# Start the daemon
		else:
			print "Derplette started on port " + str(DERPLETTE_PORT_NUM) #+ " with pid " + pid
			d = Derplette.Derplette()
			d.sendRegister()

	# -----------------------------------------------------------------
	#
	# -----------------------------------------------------------------
	def unregister(self):
		"""
		unregister from the derpmom and destroy the derplette daemon
		:return: nothing
		"""
		try:
			d = Derplette.Derplette()
			d.sendUnregister()
			
			kill_cmd = "kill `cat " + DERPLETTE_PIDFILE  + "`"
			os.system(kill_cmd)
			os.remove(DERPLETTE_PIDFILE)
			print "Derplette killed"
		except OSError:
			print 'Error: Could not unregister (perhapes no Derplette is registered?)'
	# -----------------------------------------------------------------
	# 
	# -----------------------------------------------------------------
	def generateKeys(self):
		"""
		generate RSA keys
		:return: nothing
		"""
		# TODO: generate ECC keys
		keygen_cmd = "ssh-keygen -t rsa -f " + DERPLETTE_RSA_PATH + " -q -N " + DERPLETTE_RSA_PASSPHRASE
		os.system(keygen_cmd)


	def viewTargetData(self):
		window = Tk()
		window.title("Derplette - Target Data")
		dirApp = DirectoryViewerApp.DirectoryViewerApp(window,TARGET_DATA_DIR)
		window.mainloop()		


