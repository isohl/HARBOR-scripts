""" This script will listen on a TCP socket for instruction on where to point the telescope."""
import tcp_listener_base
from Tkinter import *


class TelescopeListener(tcp_listener_base.TCPListenerBase):
	def receivePacket(self, key, value):
		try:
			print "setting telescope to altitude: %s azimuth: %s" % ( value['altitudeAngle'],  value['azimuth'] )
		except KeyError:
			pass
tcp_listener_base.startupTCPListener(TelescopeListener)