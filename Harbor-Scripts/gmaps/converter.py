import math
def tile_info(lat, lon, zoom):
    """Converts given latitude and longitude to radians"""
    rad_lat = lat / 180 * math.pi
    rad_lon = lon / 180 * math.pi

    """"""
    merc_x = rad_lon
    merc_y = math.log( math.tan(rad_lat) + 1/ math.cos(rad_lat) )
    print "Merc: "+str(merc_x)+", "+str(merc_y)
    """Converts to cartesian coordinate system"""
    cart_x = merc_x + math.pi
    cart_y = math.pi - merc_y
    print "Cartesian: "+str(cart_x)+", "+str(cart_y)
    """Determines area to display based on 256 pixels and on a sphere"""
    px0 = cart_x * 256 / (2 * math.pi )
    py0 = cart_y * 256 / (2 * math.pi )
    print "Pxy0: "+str(px0)+", "+str(py0)
    tile_x = px0 * (2 ** zoom) / 256
    tile_y = py0 * (2 ** zoom) / 256
    return int(tile_x),int(tile_y),zoom

def createURL(lat, lon, zoom):
    return "http://khm1.google.com/kh/v=89&x=%d&y=%d&z=%d&s=Ga" % tile_info(lat,lon,zoom) 

def reverseEngineer(tile_x,tile_y,zoom):
    px0 = tile_x * 256 / (2 ** zoom)
    py0 = tile_y * 256 / (2 ** zoom)

    cart_x = px0 * (2 * math.pi) / 256
    cart_y = py0 * (2 * math.pi) / 256

    merc_x = cart_x - math.pi
    merc_y = math.pi - cart_y

    rad_lat = math.sin((10 ** merc_y))
