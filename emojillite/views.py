from django.shortcuts import render
from django.http import HttpResponse
from emojillite.static.py.Satellite_parameters import cartesianToSpherical, getSatelliteByName
import json

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