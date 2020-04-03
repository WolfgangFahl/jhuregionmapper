
import csv
import requests
import datetime
from jhu.loc import Distance
from tp.gremlin import TinkerPopAble

#https://stackoverflow.com/a/35371451/1497139

class COVIDCases():
    '''
    raw time series csv data of Johns  Hopkins University at https://github.com/CSSEGISandData/COVID-19
    '''
    BASE_URL="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"

    def __init__(self):
        '''
        construct me
        '''
        self.regions={}
        
    def downloadAll(self):
        '''
        download all 5 CSV time series files
        '''
        firstKind=True
        for kind in  ["confirmed","deaths","recovered"]:
            for area in ["global","US"]:
                csv="time_series_covid19_%s_%s.csv" % (kind,area)
                if not (kind=="recovered" and area=="US"):
                    ts=TimeSeries(COVIDCases.BASE_URL+csv)
                    regionRows=ts.readCSV()
                    if firstKind:
                        firstRow=True
                        for regionRow in regionRows:
                            if not firstRow:
                                region=Region(ts,regionRow)
                                self.regions[region.rowkey]=region
                            firstRow=False    
                    firstRow=True        
                    for regionRow in regionRows:
                        if not firstRow:
                            keyRegion=Region(ts,regionRow)
                            if keyRegion.rowkey not in self.regions:
                                print ("key %s kind %s area %s invalid row %s" % (keyRegion.rowkey,kind,area,regionRow))
                            else:    
                                region=self.regions[keyRegion.rowkey]
                                region.fillTimeSeries(ts, regionRow, kind)
                        firstRow=False    
            firstKind=False     
            
class TimeSeries():
    '''
    a single time series
    '''                
    def __init__(self,csvurl):
        '''
        construct me
        '''
        self.headers={}
        self.dates=[]
        self.csvurl=csvurl
        
    def readCSV(self):    
        '''
        download the given 
        '''
        with requests.Session() as s:
            download = s.get(self.csvurl)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            regionRows = list(cr)
            firstRow=regionRows[0]
            # UID,iso2,iso3,code3,FIPS,Admin2,Province_State,Country_Region,Lat,Long_,Combined_Key,...
            for col in range(0,len(firstRow)):
                colValue=firstRow[col]
                try:
                    isodate=datetime.datetime.strptime(colValue, '%m/%d/%y').strftime('%Y-%m-%d')
                    self.dates.append(isodate)
                except ValueError:
                    self.headers[colValue]=col   
        return regionRows 

class Avg():
    ''' Average calculation '''
    def __init__(self):
        self.value=0
        self.count=0
        self.sum=0;
     
    def add(self,value):
        ''' add a value and return the new average '''
        self.count=self.count+1
        self.sum=self.sum+value
        self.value=self.sum/self.count   
        return self.value           
                
class Region(TinkerPopAble):
    '''
    a region entry in the time series
    '''
    
    debug=False
    def getField(self,ts,row,keys):
        '''
        get the field from the potential keys
        '''
        for key in keys:
            if key in ts.headers:
                return row[ts.headers[key]]
        return None   
    
    def __init__(self,ts,row):
        ''' construct me from the given row '''
        self.confirmed={}
        self.deaths={}
        self.recovered={}
        self.ts=ts
        self.lat=0
        self.lon=0
        self.latAvg=Avg()
        self.lonAvg=Avg()
        self.wikiDataId=None
        self.isocode=None
        self.pop=None
        # uncomment to debug
        # print(ts.headers)
        # print(row)
        try:
            self.province=self.getField(ts,row,['Province_State','Province/State'])
            self.country=self.getField(ts,row,['Country_Region','Country/Region'])
            self.rowkey="%s;%s" % (self.country,self.province)
            self.getLocation(ts, row)
            self.storeFields(["lat","lon","province","country","rowkey"])
        except ValueError as ve: 
            print (ve)
            raise ve
        
    def total(self,name):    
        attrList=self.__getattribute__(name)
        currentDate=self.ts.dates[len(self.ts.dates)-1]
        return attrList[currentDate]
    
    def getLocation(self,ts,row):    
        lat=float(self.getField(ts,row,['Lat']))
        lon=float(self.getField(ts,row,['Long_','Long']))    
        if (not lat*lon==0):
            self.lat=self.latAvg.add(lat)
            self.lon=self.lonAvg.add(lon)
            
    def fillTimeSeries(self,ts,row,name):
        ''' fill time series data from the given row '''    
        self.getLocation(ts, row)
        for col in range(len(ts.headers),len(row)):
            attrList=self.__getattribute__(name)
            date=ts.dates[col-len(ts.headers)]
            value=int(row[col])
            if date in attrList:
                attrList[date]=attrList[date]+value
            else:
                attrList[date]=value    
            
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
        fixname=self.rowkey
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
            self.storeFields(["pop","isocode","wikiDataId"])
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
        text= ("%32s %32s %6.1f,%6.1f" % (self.country,self.province,self.lat,self.lon))    
        return text
