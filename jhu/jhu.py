
import csv
import requests
import datetime
from jhu.loc import Distance

#https://stackoverflow.com/a/35371451/1497139

class TimeSeries():
    CSV_URL="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    
    def __init__(self):
        self.regions=[]
        self.dates=[]
        with requests.Session() as s:
            download = s.get(TimeSeries.CSV_URL)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            regionRows = list(cr)
            first=True
            for regionRow in regionRows:
                if first:
                    for col in range(4,len(regionRow)):
                        jhudate=regionRow[col]
                        isodate=datetime.datetime.strptime(jhudate, '%m/%d/%y').strftime('%Y-%m-%d')
                        self.dates.append(isodate)
                    first=False
                else:    
                    region=Region(self,regionRow)
                    self.regions.append(region)
                
class Region():
    '''
    a region entry in the time series
    '''
    debug=False
    
    def __init__(self,ts,row):
        self.confirmed={}
        #print(row)
        self.province=row[0]
        self.country=row[1]
        self.lat=float(row[2])
        self.lon=float(row[3])
        for col in range(4,len(row)):
            self.confirmed[ts.dates[col-4]]=row[col]
            
    def matchByDistance(self,regions):
        '''
        match the shortest distance region in the list of given regions
        '''
        mycoords=(self.lat, self.lon)
        mindist=40000 # once around the globe
        minregion=None # best match
        for region in regions:
            rc=(region.lat,region.lon)
            dist=Distance.distance(mycoords, rc) 
            if dist<mindist:
                minregion=region
                mindist=dist
        return minregion,mindist 
    
    def matchIsoRegion(self,regionsByWikiDataId,fixes):
        '''
        find the best matching region with IsoCode and population and copy it's data
        '''
        fixname="%s;%s" % (self.country,self.province)
        #print ("'%s'" % (fixname))
        if fixname in fixes:
            self.wikiDataId=fixes[fixname]
            if self.wikiDataId in regionsByWikiDataId:
                minregion=regionsByWikiDataId[self.wikiDataId]
                mindist=0
            else:
                minregion=None
                print("could not map %s via WikiDataId %s" % (fixname,self.wikiDataId))    
        else:
            # region independent e.g. cruise ships
            if self.lat*self.lon==0:
                self.match=1
                minregion=None
            else:    
                minregion,mindist=self.matchByDistance(regionsByWikiDataId.values())    
        self.match=0    
        if minregion is not None:
            self.isocode=minregion.isocode
            self.pop=minregion.pop
            self.wikiDataId=minregion.wikiDataId
            # if close enough assume correct e.g. on French/Netherlands islands it doesn't really matter which region is shown
            if mindist<=83:
                self.match=1
            if len(self.isocode)==2  and self.country==minregion.name:
                self.match=1        
            if len(self.isocode)>2 and self.province==minregion.name:
                self.match=1    
            if Region.debug:        
                marker="?" if self.match==0 else "✅"
            print ("%s %s - %4.0f km->%s" % (marker,self,mindist,minregion))    
        return self.match        
            
    def __str__(self):
        text= ("%22s %20s %6.1f,%6.1f" % (self.country,self.province,self.lat,self.lon))    
        return text         
        
        
        
                    
