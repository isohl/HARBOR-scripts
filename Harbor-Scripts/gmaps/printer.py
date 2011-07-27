import converter
import tcp_listener_base

from Tkinter import *


class TelescopeListener(tcp_listener_base.TCPListenerBase):
	def receivePacket(self, key, value):
		try:
			print value
			print key+":",converter.createURL(value['latitude'],value['longitude'], 10)
		except KeyError:
			pass
tcp_listener_base.startupTCPListener(TelescopeListener)
