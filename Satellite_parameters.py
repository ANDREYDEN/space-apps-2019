#input: name of the satellite as string
#output: position of the given satellite in real-time (latitude(radians), longitude(radians), altitude(kilometers))


from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from datetime import datetime as dt
import math 
from os import path

def cartesianToSpherical(x, y, z):  
    x += 6371
    #print(x, y, z)
    r = math.sqrt(x**2 + y**2 + z**2)
    if r == 0:
        pass
    elif x == 0 and y == 0:
        lat = math.pi / 2 * abs(z) / z
        lon = 0
    else:
        lat = math.acos(math.sqrt(x**2 + y**2) / r)
        lon = math.acos(x / math.sqrt(x**2 + y**2))
    alt = r - 6371
    return lat, lon, alt

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
            position = satellite.propagate(dt.now().year, dt.now().month, dt.now().day, dt.now().hour, dt.now().minute, dt.now().second)[0] #y, m, d, h, m, s
            #print(position)

    f.close()
    return cartesianToSpherical(position[0], position[1], position[2])

if __name__ == "__main__":
    pos = getSatelliteByName("OAO 2")
    print(cartesianToSpherical(pos[0], pos[1], pos[2]))