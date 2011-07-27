import re
import writetoKML
done=False

def delimit(rawdata):
    splitonce = re.split('/|h|O',rawdata)
##    print splitonce
##    splittwice = splitonce[1].rsplit('h')
##    print splittwice
    if len(splitonce)>=7:
        if 'A=' in splitonce[6]:
            returnable = [splitonce[2],splitonce[3],splitonce[6]]
            return returnable


def latlong(newdata):
##    newdata = raw_input("APRS File: ")
    if determineCompatability(newdata)==True:
        output = delimit(newdata)
        latitude = str(float(output[0][:2])+(float(output[0][2:7])/60))
        longitude = "-"+str(float(output[1][:3])+(float(output[1][3:8])/60))
        return longitude+','+latitude
    else:
        return

def determineCompatability(APRSstring):
    FILE = open('listener.txt','r')
    listenfor = FILE.read()
    listenfor = listenfor.split(',')
    FILE.close()
    if not done:
        for listento in listenfor:
            if listento in APRSstring:
                return True
    else:
        return False

##print latlong()
