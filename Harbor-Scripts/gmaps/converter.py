import math
def tile_info(lat, lon, zoom):
	rad_lat = lat / 180 * math.pi
	rad_lon = lon / 180 * math.pi

	merc_x = rad_lon
	merc_y = math.log( math.tan(rad_lat) + 1/ math.cos(rad_lat) )

	cart_x = merc_x + math.pi
	cart_y = math.pi - merc_y

	px0 = cart_x * 256 / (2 * math.pi )
	py0 = cart_y * 256 / (2 * math.pi )
	tile_x = px0 * (2 ** zoom) / 256
	tile_y = py0 * (2 ** zoom) / 256
	return int(tile_x),int(tile_y),zoom

def createURL(lat, lon, zoom):
	return "http://mt0.google.com/vt/lyrs=m@158000000&hl=en&x=%d&y=%d&z=%d&s=Ga" % tile_info(lat,lon,zoom) 