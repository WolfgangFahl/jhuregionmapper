from pyproj import Proj, transform
from geopy import distance

class Projection:
    '''
    helper to project lat/lon values to map
    '''
    @staticmethod
    def wgsToXy(lon,lat):
        return transform(Proj(init='epsg:4326'), Proj(init='epsg:3857'), lon,lat)
    
    @staticmethod
    def pointToXy(point):
        xy=point.split(",")
        return Projection.wgsToXy(float(xy[0]),float(xy[1]))
      
      
class Distance:
    '''
    helper class to calculate geographic distances
    '''
    @staticmethod
    def distance(c1,c2):
        km=40000
        try:
            km=distance.distance(c1,c2).km
        except ValueError as ve:
            pass    
        return km        