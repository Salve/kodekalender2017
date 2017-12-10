#!/usr/bin/env python3
from math import radians, cos, sin, asin, sqrt
from collections import namedtuple
from operator import methodcaller

class Hovedstad(namedtuple('Hovedstad', ['name', 'lat', 'long'])):
    __slots__ = ()
    def distance_to(self, location):
        return getDistanceFromLatLng(float(self.lat), float(self.long), float(location.lat), float(location.long))

Oslo = Hovedstad('Oslo', '59.911491', '10.757933')

# Distance between two lat/lng coordinates in km using the Haversine formula
def getDistanceFromLatLng(lat1, lng1, lat2, lng2): # use decimal degrees
# Copyright 2016, Chris Youderian, SimpleMaps, http://simplemaps.com/resources/location-distance
# Released under MIT license - https://opensource.org/licenses/MIT
    r=6371 # radius of the earth in km
    lat1=radians(lat1)
    lat2=radians(lat2)
    lat_dif=lat2-lat1
    lng_dif=radians(lng2-lng1)
    a=sin(lat_dif/2.0)**2+cos(lat1)*cos(lat2)*sin(lng_dif/2.0)**2
    d=2*r*asin(sqrt(a))
    return d # return km


with open('verda.txt') as fp:
    lines = [[field.strip() for field in line.split("\t")] for line in fp.readlines()]

filtered = [[fields[i] for i in (3, 12, 13)] for fields in lines if fields[7] == 'capital']
hovedstader = set(Hovedstad(*x) for x in filtered) # removes duplicates
sorted_hovedstader = sorted(hovedstader, reverse=True, key=methodcaller('distance_to', Oslo))

xmas_remaining = 60 * 60 * 24 # seconds
santa_speed = 7274.0 / 60 /60 # km/sec
hovedstader_visited = [] # Oslo apparently does not count

while(xmas_remaining > 0):
    next_dest = sorted_hovedstader.pop()
    distance = next_dest.distance_to(Oslo)
    reisetid = distance / santa_speed # seconds
    xmas_remaining -= reisetid # one way

    if xmas_remaining > 0:
        hovedstader_visited.append(next_dest)
        xmas_remaining -= reisetid # retur to Oslo

print(len(hovedstader_visited), hovedstader_visited)
