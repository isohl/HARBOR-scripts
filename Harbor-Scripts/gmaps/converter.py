import math
def tile_info(lat, lon, zoom):
    """Converts given latitude and longitude to radians"""
    rad_lat = lat / 180 * math.pi
    rad_lon = lon / 180 * math.pi
##    print "Radians: "+str(rad_lat)+", "+str(rad_lon)
    """"""
    merc_x = rad_lon
    merc_y = math.log( math.tan(rad_lat) + 1/ math.cos(rad_lat) )
##    print "Merc: "+str(merc_x)+", "+str(merc_y)
    """Converts to cartesian coordinate system"""
    cart_x = merc_x + math.pi
    cart_y = math.pi - merc_y
##    print "Cartesian: "+str(cart_x)+", "+str(cart_y)
    """Determines area to display based on 256 pixels and on a sphere"""
    px0 = cart_x * 256 / (2 * math.pi )
    py0 = cart_y * 256 / (2 * math.pi )
##    print "Pxy0: "+str(px0)+", "+str(py0)
    tile_x = px0 * (2 ** zoom) / 256
    tile_y = py0 * (2 ** zoom) / 256
    return int(tile_x),int(tile_y),zoom

def createURL(lat, lon, zoom):
    return "http://khm1.google.com/kh/v=89&x=%d&y=%d&z=%d&s=Ga" % tile_info(lat,lon,zoom) 

def reverseEngineer(tile_x,tile_y,zoom):
    px0 = tile_x * 256 / (2 ** zoom)
    py0 = tile_y * 256 / (2 ** zoom)
##    print "Pxy0: "+str(px0)+", "+str(py0)
    cart_x = px0 * (2 * math.pi) / 256
    cart_y = py0 * (2 * math.pi) / 256
##    print "Cartesian: "+str(cart_x)+", "+str(cart_y)
    merc_x = cart_x - math.pi
    merc_y = math.pi - cart_y
##    print "Merc: "+str(merc_x)+", "+str(merc_y)
    rad_lat = math.atan(math.sinh(merc_y))
    rad_lon = merc_x
##    print "Radians: "+str(rad_lat)+", "+str(rad_lon)
    lat = rad_lat * 18 * math.pi
    lon = rad_lon * 18 * math.pi
    return lat,lon,zoom

##latitude = float(raw_input("Latitude: "))
##longitude = float(raw_input("Longitude: "))
##zoomz = int(raw_input("zoom: "))
##
##print tile_info(latitude,longitude,zoomz)
