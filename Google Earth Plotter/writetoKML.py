import os
import decodeTNC



def writeonce(longlat,aFile):
    keepgoing=True
    while keepgoing==True:
        try:
            keepgoing=False
            os.rename( aFile, aFile+"~" )
        except WindowsError:
            try:
                os.remove(aFile+"~")
            except WindowsError:
                keepgoing=True
    try:
    ##    aFile = 'Test File.kml'
        destination= open( aFile, "w" )
        source= open( aFile+"~", "r" )
        for line in source:
            if line == '\t\t\t</coordinates>\n':
                destination.write( "\t\t\t\t"+str(longlat)+",0 \n" )
                print 'added'
            destination.write( line )
    ##        print line
    except KeyboardInterrupt:
        source.close()
        os.remove(aFile+'~')
        destination.close()
    finally:
        source.close()
        os.remove(aFile+"~")
        destination.close()


"""
while 1:
    writeonce()
    raw_input("Waiting...")
"""
