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
    Updates the file with the active satellites
'''
def getSatellites():
    r = requests.get('https://celestrak.com/NORAD/elements/active.txt')
    dirname = path.dirname(__file__)
    with open(path.join(dirname, "satellite_data_online.txt"), "w") as f:
        f.write(r.text)

'''
FUNCTION:
    Based on the name of the satellite returns its position (latitude, longitude, altitude)
ARGS:
    Name: string
RETURNS
    (float, float, float) - latitude (deg), longitude(deg), altitude(m)
'''
def getSatelliteByName(gName):
    dirname = path.dirname(__file__)
    with open(path.join(dirname, "satellite_data_online.txt"), "r") as f:
    lines = f.readlines()
    satList = {}
    satList["OAO 2"] = ("1  3597U 68110A   19297.12489875  .00000025  00000-0  12281-4 0  9997", "2  3597  34.9939 284.8592 0006194 273.1983  86.7999 14.45838868682283")
    satList["COSMOS 1500"] = ("1 14372U 83099A   19297.16869194  .00000531  00000-0  24058-4 0  9990", "2 14372  82.5177 213.9841 0014680 344.1286 144.7925 15.1852158696811")
    satList["METEOR PRIRODA"] = ("1 12585U 81065A   19296.91802554 +.00000482 +00000-0 +24609-4 0  9991", "2 12585 097.5263 280.1462 0012763 280.1951 079.7845 15.21458335086981")
    satList["OKEAN-3"] = ("1 21397U 91039A   19297.37710498  .00000201  00000-0  16892-4 0  9994", "2 21397  82.5244  42.0261 0016554 240.3541 119.6031 14.92847727537955")
    satList["TERRA"] = ("1 25994U 99068A   19297.26040016  .00000040  00000-0  19017-4 0  9994", "2 25994  98.2072   9.8444 0001348  89.0198 271.1166 14.57112096 55773")
    satList["NOAA 1"] = ("1 04793U 70106A   19297.31460843 -.00000054  00000-0 -59329-4 0  9997", "2 04793 101.6912   4.1508 0031771  39.8299   1.5411 12.53991712236847")
    satList["HST"] = ("1 20580U 90037B   19296.85414334 +.00000426 +00000-0 +14985-4 0  9996", "2 20580 028.4692 091.0449 0002859 055.0194 075.3644 15.09285106420038")
    satList["INTERCOSMOS 24"] = ("1 20261U 89080A   19296.65408977 +.00000020 +00000-0 +53449-5 0  9991", "2 20261 082.6104 174.1727 1201839 276.5618 070.0353 12.56111104374141")
    satList["RESURS-DK 1"] = ("1 29228U 06021A   19296.87860892  .00000079  00000-0  13304-4 0  9998", "2 29228  69.9354  72.7708 0001794 132.4194 227.7118 15.02475204737068")
    if r.text.find(gName + " ") == -1:
        line1 = satList[gName][0]
        line2 = satList[gName][1]
    else:
        line1 = r.text[r.text.find(gName + " ") + 26 : r.text.find(gName + " ") + 95]
        line2 = r.text[r.text.find(gName + " ") + 97 : r.text.find(gName + " ") + 166]
        #print(gName)
        #print(line1)
        #print(line2)
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
   print("NOAA 19", getSatelliteByName("RESURS-DK 1"))
