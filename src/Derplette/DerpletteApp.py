#--------------------------------------------------------------------------------
#
#Derp GUI in python TK
#Team 143
#
#--------------------------------------------------------------------------------

# For stuff involving TK
from Tkinter import *


from libs.pygmaps import maps
from pygeoip import GeoIP
import os, sys, re, webbrowser, errno, socket, subprocess
from time import gmtime, strftime

# Data Classes
import data.Coordinates
import data.Port
import data.Service
import data.TargetData
import data.Timestamp
import data.parseXML
import data.DirectoryViewerApp

# Derp class
import Derplette, DerpletteDaemon
from DERPLETTE_CONFIG import *

class DerpletteApp:
	IP = '' #Next items are created for simple transfer of data
	hostName = ''
	ports = {}
	state = ''
	def __init__(self,root): #define wndow
        
		frame = Frame(root)
		frame.pack()
	
		self.target_label = Label(frame, text="Target:")
		self.target_label.grid(row=0, column=0, columnspan=1)
        
		self.target = StringVar() #target box
		self.textbox = Entry(frame,textvariable=self.target)
		self.target.set("IP or Hostname")
		self.textbox.grid(row=0, column=1, columnspan=4)

		self.target_label = Label(frame, text="NMAP Args:")
		self.target_label.grid(row=1, column=0, columnspan=1)

		self.target = StringVar() #argument box
		self.textbox1 = Entry(frame,textvariable=self.target)
		self.target.set("NMAP ARGUMENTS")
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

	def scanit(self): #funtion to scan on record results
		flag = True
		gic = GeoIP(GEOIP_DATABASE) #change this to the location of GeoLiteCity.dat
		flag = False
		target = self.textbox.get()
		args = self.textbox1.get()
		if target != '': #error checking (not empty string)
			try:
				targetIP = socket.gethostbyname(target) #attempts to get an ip from hostnam/ip passed through 
				gic = GeoIP(GEOIP_DATABASE) #load geoIP database
				addr = gic.record_by_addr(targetIP) #if this works (getting ip) find address of ip
				try: #try to get longatudinal and latitudinal coordanates
					addr['latitude']
					addr['longitude']
				except TypeError:  #if ip has no address (like 127.0.0.1) set lat and lng to 0,0
					lat = 0
					lng = 0
				else: #else set them to correct coordanates
					lat = addr['latitude']
					lng = addr['longitude']

			except socket.gaierror: #if finding IP fails
				print 'ERROR: Counld not get ip from hostname'
				lat = 0
				lng = 0
				return
			xmlPath =  TARGET_XML + targetIP + '.xml'
			htmlPath = TARGET_HTML + targetIP + '.html'
			mymap = maps(lat,lng,16) #create google map file
			mymap.addradpoint(lat, lng, 100, "#0000FF")
			mymap.draw(htmlPath)
			if lng != 0 and lat !=  0:
				webbrowser.open(htmlPath)
			if args == 'NMAP ARGUMENTS': #error checking
				args = ''
			messege = ''
			if '-sV' not in args:
				args = args + ' -sV '
			if '-oX' not in args:
				args += ' -oX ' + xmlPath
				command = 'nmap ' + args + ' ' + targetIP + ' > /dev/null';
				returnValue = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
				returnValue.wait()
				#os.system('nmap ' + args + ' ' + targetIP + ' > /dev/null') 
				tempDict = {}
				runTime,hostName,HostIP,tempDict = data.parseXML.parseMyXML(xmlPath)
			
				# Create a target DATA 
				target_data = self.createTargetData(targetIP, tempDict, hostName, lat, lng)
				
				# Write the TargetData to a file
				target_data.serializeToFile(target_data.ip_addr, TARGET_DATA_DIR)

				# Send the target data to the derp mom
				try:
					d = Derplette.Derplette()
					d.sendTargetData(target_data)
				except socket.error as e:
					if e.errno == errno.ECONNREFUSED:
						print "Could not connect to DerpMom...."		
			else:
				print 'ERROR: Cannot use -oX option (we already did that for you).'
    

	# -------------------------------------------------------------
	#  Create Target Data
	#
	#	This function takes an IP Address, NMAP PortScanner, 
	# 		and two coordinates and creates a TargetDataObject 
	# --------------------------------------------------------------
	def createTargetData(self, targetIP, tempDict, hostName, lat, lng):
  
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

	# -----------------------------------------------------------------
	#  Register
	# -----------------------------------------------------------------
	def register(self):

		retval = os.fork()

		if retval == 0:
			# Start the daemon
			daemon = DerpletteDaemon.DerpletteDaemon(DERPLETTE_PIDFILE)
			daemon.start()
		else:

			print "Derplette started on port " + str(DERPLETTE_PORT_NUM) #+ " with pid " + pid 
 
			d = Derplette.Derplette()
			d.sendRegister()

	# -----------------------------------------------------------------
	#
	# -----------------------------------------------------------------
	def unregister(self):
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

		keygen_cmd = "ssh-keygen -t rsa -f " + DERPLETTE_RSA_PATH + " -q -N " + DERPLETTE_RSA_PASSPHRASE
		os.system(keygen_cmd)


	def viewTargetData(self):

		window = Tk()
		window.title("Derplette - Target Data")
		dirApp = DirectoryViewerApp.DirectoryViewerApp(window,TARGET_DATA_DIR)
		window.mainloop()		


