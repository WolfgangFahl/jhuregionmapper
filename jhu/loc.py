from pyproj import Proj, CRS,transform
from geopy import distance

class Projection:
    '''
    helper to project lat/lon values to map
    '''
    #e4326=Proj(init='epsg:4326')
    e4326=CRS('EPSG:4326')
    #e3857=Proj(init='epsg:3857')
    e3857=CRS('EPSG:3857')
    
    @staticmethod
    def wgsToXy(lon,lat):
        t1=transform(Projection.e4326,Projection.e3857, lon,lat)
        #t2=transform(Proj('epsg:4326'), Proj('epsg:3857'), lon,lat)
        return t1
    
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