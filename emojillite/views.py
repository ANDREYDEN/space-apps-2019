from django.shortcuts import render
from Satellite_parameters import cartesianToSpherical, getSatelliteByName
from math import pi

SATELLITES = ['OAO 2', 'NOAA1', 'NOAA2']

def index(request):
    pos = getSatelliteByName(SATELLITES[0])
    lat, lng, alt = cartesianToSpherical(pos[0], pos[1], pos[2])
    context = {
        'lat' : float(lat/pi*180),
        'lng' : float(lng/pi*180),
        'alt' : float(alt*1000)
    }
    return render(request, "index.html", context)
