import os
import writetoKML
import socket
import json
import decodeTNC
from Tkinter import *
done=False
##acceptedSigns = ['KE7ROS','WB1SAR','N7RPG','KD7FDH']
##ip=raw_input("IP of server: (.local does not work) ")
##port=int(raw_input("Port of server: (default-54730 series) "))
##if ip == "": ip='192.168.1.21'
##if port == "": port=54730
##if port<10: port=54730+port


class Application(Frame):
        def submit(self,event):
                self.ip=self.ipaddress.get()
                if self.ip.lower() == "local":
                    self.localonly=True
                    print "Entering Local Mode"
                else:
                    self.localonly=False
                    print "Entering Socket Mode"
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
                self.ipaddress.bind('<Return>',self.submit)
                self.portaddress = Entry(self, justify=CENTER)
                self.portaddress.pack()
                self.portaddress.insert(0,54730)
                self.portaddress.bind('<Return>',self.submit)
                self.listeners = Entry(self, justify=CENTER,width=50)
                self.listeners.pack()
                self.listeners.insert(0,"KE7ROS, WB1SAR, N7RPG, KD7FDH, KE7WHZ, $PKWDPOS")
                self.listeners.bind('<Return>',self.submit)
##                self.submiter = Button(self)
##                self.submiter["text"] = "Submit",
##                self.submiter["command"] = self.submit("YAY")
##
##                self.submiter.pack()

        def __init__(self, master=None):
                self.localonly=False
                Frame.__init__(self, master)
                self.pack()
                self.createWidgets()






        def main(self):
                try:
                        savedtime=0
                        if self.localonly==False:
                            server = socket.socket()
                            server.connect((self.ip,self.port))
                        else:
                                if os.name=="nt":
                                    filepath = os.path.expanduser('~')+"\\tnclogs\\tnc.log"
                                elif os.name=="posix":
                                        filepath = os.path.expanduser("~/Documents/tnc.log")
                                else:
                                        print "UNKNOWN OPERATING SYSTEM. GET A LIFE."
                                f = open(filepath)
                                savedtime=os.stat(filepath).st_mtime
                        print "Successfully Connected"
                        while not done:
                                incoming = ''
                                if self.localonly==True:
                                    time = os.stat(filepath).st_mtime
                                    while time==savedtime:
                                        time = os.stat(filepath).st_mtime                                    
                                    savedtime=time
                                    f.close()
                                    f = open(filepath,'r')
                                    print "Retrieving data"
                                    #find last line
                                    allLines = f.readlines()
                                    lastline = allLines[len(allLines)-1]
                                    print lastline
                                    try:
                                        compatible, listento = decodeTNC.determineCompatability(lastline,self.acceptedSigns)
                                        if compatible == True:
                                            if "PKWDPOS" in listento:listento='d710'
                                            lon,lat = decodeTNC.latlong(lastline)
                                            incoming={listento:{'latitude':lat,'longitude':lon}}
                                            print incoming
                                            
                                    except TypeError:
                                                print "Unsolved TypeError, sucks to be you!"
##                                    except TypeError:

                                else:
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
                                if incoming != '':
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
                                                                    print lat
                                                                    print lon
                                                                    writetoKML.writeonce((str(lon)+","+str(lat)),afile)
                                                            except KeyError:
                                                                    print "No Latitude or Longitude"
                                            if write==True:
                                                    break

                except KeyboardInterrupt:
                    if self.localonly!=True:
                        server.close()
                        print "Closed"
                        

                except socket.herror:
                        print "Invalid address"
                finally:
                    if self.localonly!=True:
                        server.close()
                        print "Closed"



root = Tk()
##root.geometry("500x500")
app = Application(master=root)
app.mainloop()
