import decodeTNC
import writetoKML
import os
import linecache

filepath = '/Users/Ian/Documents/My Dropbox/saved_tnc.log/testTNC.log'
print "Monitoring "+str(filepath)
FILE = open(filepath,'r')
savedtime = os.stat(filepath).st_mtime
lastline = ''
while 1:
    time = os.stat(filepath).st_mtime
##    print "Waiting..."
    if time!=savedtime:
        savedtime=time
        print "Updated"
        FILE.close()
        FILE = open(filepath,'r')
        print "Retrieving data"
        #find last line
        linecount = 0
        seekbit = []
        offset = 0
        for line in FILE:
            linecount+=1
            seekbit.append(offset)
            offset+=len(line)
        print str(linecount)+" lines"
        print seekbit
        FILE.seek(seekbit[linecount-1])
        lastline = FILE.read()
        print lastline
        longlat = decodeTNC.latlong(lastline)
        writetoKML.writeonce(longlat)
        print "Map Updated"
