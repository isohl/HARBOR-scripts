import socket
import json
import time

soc=socket.socket()
soc.connect(("xibook.local",54730))
everybody={}
keys=[]
try:
        while 1:
                try:
                        got=json.loads(soc.recv(1024))
                except Exception as e:
                        print e
                for key in got:
                        if key in ["KE7ROS-11","WB1SAR-11","D710"]:
                                try:
                                        keys.remove(key)
                                except ValueError:
                                        pass
                                keys.insert(0,key)
                                try:
                                        got[key]['old']=everybody[key]
                                except KeyError:
                                        pass
                                everybody[key]=got[key]
                                print "\n\n"
                for key in keys:
                        currTime=time.ctime(everybody[key]['time'])
                        uprate=""
                        try:
                                pass
                                #diff=everybody[key]['time']-everybody[key]['old']['time']
                                #diffAlt=everybody[key]['altitude']-everybody[key]['old']['altitude']
                                #uprate="ascending at: "+str(diffAlt/diff*3.28)+"ft/s"
                        except KeyError, ZeroDivisionError:
                                pass
                        print key+":",currTime,"path:",everybody[key]['path']
                        try:
                                print "lat/lon:",everybody[key]['latitude'],"/",everybody[key]['longitude']
                        except KeyError:
                                print
                        try:
                                print "Altitude:",everybody[key]['altitude'],"m",everybody[key]['altitude']*3.28,'ft',uprate
                        except KeyError:
                                print
                
except KeyboardInterrupt:
        soc.close()
