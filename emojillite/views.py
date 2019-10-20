from django.shortcuts import render
from Satellite_parameters import cartesianToSpherical, getSatelliteByName
from math import pi

SATELLITES = {'OAO 2': 'star.png',
     'NOAA 1': 'atmosphere.png',
     'METEOR PRIRODA': 'temperature.png',
     'COSMOS 1500': 'ocean.png',
     'AJISAI (EGS)': 'earth.png',
     'INTERCOSMOS 24': 'antenna.png',
     'HST': 'telescope.png',
     'OKEAN-3': 'ice.png',
     'TERRA': 'climate.png',
     'RESURS-DK 1': 'agriculture.png'}

def index(request):
    sats = []
    for name in SATELLITES:
        lat, lng, alt = getSatelliteByName(name)
        sats.append((str(round(float(lat/pi*180), 3)) + " " +
                     str(round(float(lng/pi*180), 3)) + " " +
                     str(round(float(alt*1000), 3)) + " " +
                     SATELLITES[name] + " " + name))

    return render(request, "index.html", {'satellites': sats})
