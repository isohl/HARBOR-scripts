""" This script will listen on a TCP socket for instruction on where to point the telescope."""
import tcp_listener_base
from Tkinter import *


class TelescopeListener(TCPListenerBase):
	def receivePacket(self, key, value):
		print key, value

root = Tk()
app = TelescopeListener(master=root)
app.mainloop()