from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime as dt
from math import sqrt, atan, degrees, pi
from os import path
import requests

'''
FUNCTION:
    Converts (x, y, z) point into (latitude, longitude, altitude)
ARGS:
    x: float, y: float, z: float - coordinates (km)
RETURNS
    (float, float, float) - latitude (deg), longitude (deg), altitude (m)
'''
def cartesianToSpherical(x, y, z):   #x, y, z - center of the Earth
    r = sqrt(x**2 + y**2 + z**2)
    lat = lon = alt = 0
    if x == 0 and y == 0:
        if z != 0:
            lat = pi / 2 * abs(z) / z
            lon = 0
    else:
        if x != 0:
            lat = atan(z / sqrt(x**2 + y**2))
            lon = atan(y / x)
            if x < 0 and y > 0:
                lon += pi
            if x < 0 and y < 0:
                lon = lon - pi
        else:
            lat = atan(z / sqrt(x**2 + y**2))
            lon = pi / 2 * abs(y) / y
    alt = r - 6371
    return degrees(lat), degrees(lon), alt * 1000


'''
FUNCTION:
    Based on the name of the satellite returns its position (latitude, longitude, altitude)
ARGS:
    Name: string
RETURNS
    (float, float, float) - latitude (deg), longitude(deg), altitude(m)
'''
def getSatelliteByName(gName):
    r = requests.get('https://celestrak.com/NORAD/elements/active.txt')
    dirname = path.dirname(__file__)
    f = open(path.join(dirname, "satellite_data_online.txt"), "w")
    f.write(r.text)
    f.close()
    f = open(path.join(dirname, "satellite_data_online.txt"), "r")
    lines = f.readlines()
    f.close()
    satList = {}
    line1 = r.text[r.text.find(gName + " ") + 26 : r.text.find(gName + " ") + 95]
    line2 = r.text[r.text.find(gName + " ") + 97 : r.text.find(gName + " ") + 166]
    print(gName)
    print(line1)
    print(line2)
    '''
    for x in range(0, len(lines) - 5, 6):
        satList[lines[x].strip()] = (lines[x + 2].strip(), lines[x + 4].strip())
    #for x in range(0, len(lines) - 2, 3):
     #   satList[lines[x].strip()] = (lines[x + 1].strip(), lines[x + 2].strip())
    position = [0, 0, 0]
    line1, line2 = satList[gName]
    '''
    satellite = twoline2rv(line1, line2, wgs72)
    position = satellite.propagate(dt.utcnow().year, dt.utcnow().month, dt.utcnow().day, dt.utcnow().hour, dt.utcnow().minute, dt.utcnow().second)[0]
    return cartesianToSpherical(position[0], position[1], position[2])

if __name__ == "__main__":
   print("NOAA 19", getSatelliteByName("NOAA 19"))
