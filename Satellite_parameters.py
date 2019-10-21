from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime as dt
from math import sqrt, atan, degrees, pi
from os import path

'''
FUNCTION:
    Converts (x, y, z) point into (latitude, longitude, altitude)
ARGS:
    x: float, y: float, z: float - coordinates
RETURNS
    (float, float, float) - latitude (deg), longitude (deg), altitude (m)
'''
def cartesianToSpherical(x, y, z):  
    r = sqrt(x**2 + y**2 + z**2)
    lat = lon = alt = 0
    if r == 0:
        pass
    elif x == 0 and y == 0:
        lat = pi / 2 * abs(z) / z
        lon = 0
    else:
        lat = atan(z / sqrt(x**2 + y**2))
        lon = atan(y / x)
        if x < 0 and y > 0:
            lon += pi
        if x < 0 and y < 0:
            lon = lon - pi
    alt = r - 6371
    return degrees(lat), degrees(lon), alt * 1000

def getSatelliteByName(gName):
    dirname = path.dirname(__file__)
    f = open(path.join(dirname, "satellite_data.txt"), "r")
    lines = f.readlines()
    satList = []
    for x in range(0, len(lines) - 2, 3):   
        satList.append({"name": lines[x].strip(), "satLine1": lines[x + 1].strip(), "satLine2": lines[x + 2].strip()})
     
    position = 0
    for x in satList:
        if x["name"] == gName:
            line1 = x["satLine1"]
            line2 = x["satLine2"]
            satellite = twoline2rv(line1, line2, wgs72)
            #print(dt.now().year, dt.now().month, dt.now().day + (dt.now().hour + 4) // 24, (dt.now().hour + 4) % 24, dt.now().minute, dt.now().second)
            position = satellite.propagate(dt.now().year, dt.now().month, dt.now().day + (dt.now().hour + 4) // 24, (dt.now().hour + 4) % 24, dt.now().minute, dt.now().second)[0] #y, m, d, h, m, s
            #print("pos", position)
    f.close()
    return cartesianToSpherical(position[0], position[1], position[2])

def sphtocar(lat, lon, alt):
    earthRadius = 6371 + alt
    x = earthRadius * cos(lat)*cos(lon)
    y = earthRadius * cos(lat)*sin(lon)
    z = earthRadius * sin(lat)
    r = sqrt(x**2 + y**2 + z**2)
    return x, y, z

#print(sphtocar(38 /180*3.14, 62 /180*3.14, 421))

if __name__ == "__main__":
    pos = getSatelliteByName("OAO 2")
    print(pos[0]*180/3.14, pos[1]*180/3.14, pos[2])
    #print("test", (pos[0] * 180 /3.14, pos[1] *180 /3.14, pos[2]))
