from django.shortcuts import render
from Satellite_parameters import cartesianToSpherical, getSatelliteByName
from math import pi

SATELLITES = ['OAO 2', 'NOAA 1', 'NOAA 2 (ITOS-D)', 'ISIS 1', 'SERT 2']

def index(request):
    sats = []
    for name in SATELLITES:
        lat, lng, alt = getSatelliteByName(name)
        sats.append((str(round(float(lat/pi*180), 3)) + " " +
                     str(round(float(lng/pi*180), 3)) + " " +
                     str(round(float(alt*1000), 3))))

    return render(request, "index.html", {'satellites': sats})
