""" This script will listen on a TCP socket for instruction on where to point the telescope."""
import socket
import json
from Tkinter import *


class TCPListenerBase(Frame):
	""" Subclasses should override these methods if the want to stay informed."""
	def receivePacket(self, key, value):
		print key, value
	def jsonFail(self, packet):
		print "BAD JSON"
		print packet
	
	def connectSuccess(self):
		print "Successfully Connected"	
	
	def portChanged(self, newport):
		print "Opened new port: "+str(newport)
	
	def didClose(self):
		print "Closed"	
	def gotRawPacket(self, packet):
		pass
	
	
	
	
	"""Internals do not override."""
	
	def submit(self):
		self.ip=self.ipaddress.get()
		self.port=int(self.portaddress.get())
		self.acceptedSigns = self.listeners.get()
		self.acceptedSigns=self.acceptedSigns.split(', ')
		self.main()
    
	def createWidgets(self):
		self.instructions = Label(self)
		self.instructions["text"] = "IP and port of server"
		
		self.instructions.pack({"side": "top"})
		
		self.ipaddress = Entry(self, justify=CENTER)
		self.ipaddress.pack()
		self.ipaddress.insert(0,"xibook.local")
		
		self.portaddress = Entry(self, justify=CENTER)
		self.portaddress.pack()
		self.portaddress.insert(0,54730)
		
		self.listeners = Entry(self, justify=CENTER,width=50)
		self.listeners.pack()
		self.listeners.insert(0,"KE7ROS, WB1SAR, N7RPG, KD7FDH, KE7WHZ")
		
		self.submiter = Button(self)
		self.submiter["text"] = "Submit",
		self.submiter["command"] = self.submit
		
		self.submiter.pack()
	
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
	
	def stop(self):
		self.done=True
	
	def main(self):
		try:
			server = socket.socket()
			server.connect((self.ip,self.port))
			self.connectSuccess()
			self.done=False
			while not self.done: 
				incoming = server.recv(1000)
				if incoming == "": break
				try:
					incoming=json.loads(incoming)
				except ValueError:
					self.jsonFail(incoming)
					continue
				self.gotRawPacket(incoming)
				for sign in self.acceptedSigns:
					write=False
					for callsign in incoming:
						if sign.lower() in callsign.lower():
							self.receivePacket(sign, incoming[sign])
						elif 'port change notification' in callsign.lower():
							newport=incoming[callsign]
							server.close()
							del(server)
							server=socket.socket()
							server.connect((self.ip,newport))
							self.portChanged(newport)
		except KeyboardInterrupt:
			pass
		
		except socket.herror:
			print "Invalid address"
		
		finally:
			server.close()
			self.didClose()
			self.master.quit()



	
def startupTCPListener(listener):
	root = Tk()
	app = listener(master=root)
	app.mainloop()