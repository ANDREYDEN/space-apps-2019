from django.shortcuts import render
from Satellite_parameters import cartesianToSpherical, getSatelliteByName
from math import pi

class Satellite:
  def __init__(self, lat, lng, alt):
    self.lat = lat
    self.lng = lng
    self.alt = alt

  def calc(self):
    self.stats = (str(round(float(self.lat/pi*180), 3)) + " " +
                    str(round(float(self.lng/pi*180), 3)) + " " +
                    str(round(float(self.alt/pi*180), 3)))
    return self.stats

def index(request):
    pos = getSatelliteByName("OAO 2")
    lat, lng, alt = cartesianToSpherical(pos[0], pos[1], pos[2])
    # context = {
    #     'lat' : round(float(lat/pi*180), 3),
    #     'lng' : round(float(lng/pi*180), 3),
    #     'alt' : round(float(alt*1000), 3)
    # }
    aoa2 = Satellite(lat, lng, alt)
    aoa2 = aoa2.calc()
    return render(request, "index.html", {'aoa2' : aoa2})