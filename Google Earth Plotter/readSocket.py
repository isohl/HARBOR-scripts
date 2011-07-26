import writetoKML
import socket
import portnum
import json
from Tkinter import *
done=False
##acceptedSigns = ['KE7ROS','WB1SAR','N7RPG','KD7FDH']
##ip=raw_input("IP of server: (.local does not work) ")
##port=int(raw_input("Port of server: (default-54730 series) "))
##if ip == "": ip='192.168.1.21'
##if port == "": port=54730
##if port<10: port=54730+port



class Application(Frame):
        def submit(self):
                self.ip=self.ipaddress.get()
                self.port=int(self.portaddress.get())
                self.acceptedSigns = self.listeners.get()
                self.acceptedSigns=self.acceptedSigns.split(', ')
                print self.ip
                print self.port
                print self.acceptedSigns
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






        def main(self):
                try:
                        server = socket.socket()
                        server.connect((self.ip,self.port))
                        print "Successfully Connected"
                        while not done: 
                                incoming = server.recv(1000)
                                if incoming == "": break
##                                print incoming
                                try:
                                        incoming=json.loads(incoming)
                                except ValueError:
                                        print "BAD JSON"
                                        print incoming
                                        continue
                                print incoming
                                for sign in self.acceptedSigns:
                                        write=False
                                        for callsign in incoming:
                                                if sign.lower() in callsign.lower():
                                                        write=True
##                                                        print "Found Balloon Signature"
                                                        afile="Balloon Track.kml"
                                                elif 'd710' in callsign.lower():
                                                        write=True
##                                                        print "Found D710 Signature"
                                                        afile="D710 Track.kml"
                                                elif 'port change notification' in callsign.lower():
                                                        newport=incoming[callsign]
                                                        server.close()
                                                        print "Closing old port"
                                                        del(server)
                                                        server=socket.socket()
                                                        server.connect((self.ip,newport))
                                                        print "Opened new port: "+str(newport)
                                                if write==True:
                                                        try:
                                                                lat=incoming[callsign]['latitude']
                                                                lon=incoming[callsign]['longitude']
##                                                                print lat
##                                                                print lon
                                                                writetoKML.writeonce((str(lon)+","+str(lat)),afile)
                                                        except KeyError:
                                                                print "No Latitude or Longitude"
                                        if write==True:
                                                break

                except KeyboardInterrupt:
                        server.close()
                        print "Closed"
                        

                except socket.herror:
                        print "Invalid address"
                finally:
                        server.close()
                        print "Closed"



root = Tk()
##root.geometry("500x500")
app = Application(master=root)
app.mainloop()
