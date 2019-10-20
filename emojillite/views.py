from django.shortcuts import render
from Satellite_parameters import cartesianToSpherical, getSatelliteByName
from math import pi

SATELLITES = ['OAO 2', 'NOAA 1', 'NOAA 2 (ITOS-D)']

class Satellite:
  def __init__(self, name):
    pos = getSatelliteByName(name)
    self.lat, self.lng, self.alt = cartesianToSpherical(pos[0], pos[1], pos[2])

  def calc(self):
    self.stats = (str(round(float(self.lat/pi*180), 3)) + " " +
                    str(round(float(self.lng/pi*180), 3)) + " " +
                    str(round(float(self.alt/pi*180), 3)))
    return self.stats

def index(request):
    sats = [Satellite(sat).calc() for sat in SATELLITES]
    return render(request, "index.html", {'sats': sats})