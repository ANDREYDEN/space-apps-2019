from django.shortcuts import render
from django.http import HttpResponse
from emojillite.static.py.Satellite_parameters import cartesianToSpherical, getSatelliteByName, getSatellites
import json

SATELLITES = {'GENESIS 1': 'star.png',
     'CICERO 8': 'atmosphere.png',
     'NOAA 9': 'temperature.png',
     'OCEANSAT-2': 'ocean.png',
     'STARLETTE': 'earth.png',
     'RADARSAT-2': 'antenna.png',
     'HST': 'telescope.png',
     'CRYOSAT 2': 'ice.png',
     'TERRA': 'climate.png',
     'RESURS-DK 1': 'agriculture.png'}

def index(request):
    getSatellites()
    satellites = {}
    for name in SATELLITES:
        lat, lng, alt = getSatelliteByName(name)
        satellites[name] = {'lat': lat, 'lng': lng,
                            'alt': alt, 'img': SATELLITES[name]}

    return render(request, "index.html", {'satellites': json.dumps(satellites)})

def coords(request, name): 
    try:
        return HttpResponse(json.dumps(getSatelliteByName(name)))
    except TypeError:
        return HttpResponse(None)
