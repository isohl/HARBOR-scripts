from pictureMerger import *

def runByFolder():
    originx = int(raw_input("Originx: "))
    originy = int(raw_input("Originy: "))
    tilesEast = int(raw_input("TilesEast: "))
    tilesSouth = int(raw_input("TilesSouth: "))
    furthest1 = int(raw_input("Furthest1: "))
    furthest2 = int(raw_input("Furthest2: "))
    furthest = (furthest1,furthest2)
    defaultPath = raw_input("defaultPath: 
    final = Image.new("RGB",(tilesEast*256+tilesEast,tilesSouth*256+tilesSouth),"Black")
    stop=False
    for x in range(tilesEast):
        for y in range(tilesSouth):
            if (x,y) == furthest:
                stop = True
            newframe = Image.open(str(defaultPath)+"x"+str(originx+x)+" y"+str(originy+y)+" z"+str(zoomz)+".jpg")
            final.paste(newframe,(x*257,y*257))
            print "Combined: "+str(x)+", "+str(y)
            if stop==True:
                break
        if stop==True:
            break
    final.save(str(defaultPath)+"final"+str(NWcorner)+" z"+str(zoomz)+".jpg")
    print "Saved final image"
