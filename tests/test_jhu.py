'''
Created on 2020-03-28

@author: wf
'''
import unittest
import getpass
import datetime
import pytz
import os
from pathlib import Path
from tp.gremlin import RemoteGremlin, TinkerPopAble
from jhu.pop import ISORegion
from jhu.jhu import COVIDCases
from jhu.jhu import Region
from jhu.loc import Projection
from jhu.map import WorldMap
from jhu.pygalmap import PWorldMap

class JohnsHopkinsRegionMappingTest(unittest.TestCase):
    '''
    test mapping johns hopkins covid-19 data province/country region mapping
    via access to a janus graph docker instance using the RemoteGremlin helper class
    '''

    def setUp(self):
        '''
        setUp the environment for the test
        '''
        # uncomment if you'd like to debug parts of the tests
        RemoteGremlin.debug=True
        # default server for janusgraph instance
        self.gremlinserver="localhost"
        # default sharepoint 
        self.sharepoint=str(Path.home())+"/graphdata/"
        # developer's environment
        # adapt to your own username and needs
        if getpass.getuser()=="wf":
            self.gremlinserver="capri.bitplan.com"
            self.sharepoint="/Volumes/bitplan/user/wf/graphdata/"
        # open the remote gremlin connection and set up the share point    
        self.rg = RemoteGremlin(self.gremlinserver)
        self.rg.open()
        self.rg.sharepoint(self.sharepoint, "/graphdata/")
        pass

    def tearDown(self):
        '''
        after finishing close the remote connection
        '''
        self.rg.close()
        pass
    
    def clean(self):
        '''
        clean the graph database by removing all edges and vertices
        '''
        # get the vertices
        gV = self.rg.g.V()
        # drop the existing content of the graph
        #gV.E().drop().iterate()
        gV.V().drop().iterate()
    
    def testJanusGraph(self):
        '''
        test communication to janus Graph
        '''
        self.clean()
        # we have a traversal now
        # assert isinstance(gV,GraphTraversal)
        # convert it to a list to get the actual vertices
        vList = self.rg.g.V().toList()
        print (len(vList))
        assert len(vList) == 0
        pass
    
    def test_loadGraph(self):
        '''
        test loading a graph ml database
        '''
        self.clean()
        g = self.rg.g
        graphmlFile = "air-routes-small.xml";
        for path in [".","tests"]:
            graphmlPath=path+"/"+graphmlFile
            if os.path.isfile(graphmlPath):
                shared = self.rg.share(graphmlPath)
        # read the content from the air routes example
        g.io(shared).read().iterate()
        vCount = g.V().count().next()
        print ("%s has %d vertices" % (shared, vCount))
        assert vCount == 47
    
    def test_saveGraph(self):
        '''
        test saving a simple graph with a single vertex to a graphml file
        '''
        self.clean()
        g = self.rg.g
        g.addV("country").property("name", "Germany").iterate()
        gfile = "countries.xml"
        g.io(self.rg.sharepath + gfile).write().iterate()
        self.assertTrue(os.path.isfile(self.rg.sharepoint + gfile))
        
    def test_CacheISORegions(self):
        '''
        test caching region information retrieved from WikiData via a SPARQL query
        '''
        self.clean()
        gfile = "isoregions.xml"
        cachefile=TinkerPopAble.cache(self.rg, gfile, ISORegion, ISORegion.regions, ISORegion.fromWikiData)  
        # we check the number of regions expected here - please adapt if the
        # SPARQL query or WikiData content changes
        self.assertTrue(422<=len(ISORegion.regions))
        self.assertTrue(os.path.isfile(cachefile),cachefile)
        pass    
    
    def test_JHU_Regions(self):
        ''' test getting the names from John Hopkins university 
        time series data country and province'''
        cases = COVIDCases()
        cases.downloadAll()
        cases.display()
        
    def test_MatchRegions(self):
        '''
        test matching Johns Hopkins University regions to WikiData retrieved Region info by
        lat/lon distance
        '''
        self.clean()
        gfile = "isoregions.xml"
        TinkerPopAble.cache(self.rg, gfile, ISORegion, ISORegion.regions, ISORegion.fromWikiData) 
        print ("cached %3d ISO regions (from WikiData)" % (len(ISORegion.regions)))
        cases = COVIDCases()
        cases.downloadAll()
        print ("loaded %3d case regions (from Johns Hopkins University)" % (len(cases.regions.values())))    
        Region.debug = True
        matches = 0
        fixes = {"US;":"Q30", "Germany;":"Q183", "United Kingdom;": "Q145", "Netherlands;":"Q29999", "Norway;":"Q20", "Holy See;":"Q237", "Korea, South;":"Q884", "Taiwan*;":"Q57251",
                 "Denmark;Greenland":"Q223",
                 "Australia;Queensland":"Q36074","Australia;South Australia":"Q35715","Australia;Northern Territory":"Q3235",
                 "Australia;New South Wales":"Q3224",
                 "Canada;British Columbia":"Q1974",
                 "China;Chongqing":"Q19770","China;Tibet":"Q17269","China;Tianjin":"Q21208","China;Shanghai":"Q148",
                 "China;Ningxia":"Q57448","China;Beijing":"Q148",
                 "Cabo Verde;":"Q1011",
                 "Congo (Brazzaville);":"Q974","Congo (Kinshasa);":"Q974",
                 "France;French Polynesia":"Q30971",
                 "Cameroon;":"Q1009", "Mauritania;":"Q1025","Burma;":"Q836", "Malaysia;":"Q833",
        # US
                 "US;Northern Mariana Islands":"Q16644",
        # political incorrect ?
                 "Kosovo;":"Q403","West Bank and Gaza;":"Q801",
        # exotic case Cruise ship with lat/lon - in Oakland California ...
                 "Canada;Grand Princess":"Q99"
        }
        isoRegionsByWikiDataId = {}
        for iregion in ISORegion.regions:
            isoRegionsByWikiDataId[iregion.wikiDataId] = iregion
        for region in cases.regions.values():
            matches = matches + region.matchIsoRegion(isoRegionsByWikiDataId, fixes)
        print ("found %3d matches" % (matches))    
        gfile = "jhuregions.xml"
        cachefile=TinkerPopAble.cache(self.rg, gfile, Region, cases.regions.values(), self.void)  
        self.assertTrue(os.path.isfile(cachefile),cachefile)
    
    def void(self):
        # do nothing
        pass
            
    def testProjection(self):
        '''
        test the mercator projection
        '''
        point="-0.1285907, 51.50809"
        coords=Projection.pointToXy(point)
        x1,y1=coords
        coords=Projection.wgsToXy(-0.1285907, 51.50809) # longitude first, latitude second.
        x2,y2=(coords)
        self.assertEquals(x1,x2) 
        self.assertEquals(y1,y2) 
        
    def testMap(self):
        '''
        test plotly scattermap of today's data
        '''
        if getpass.getuser()!="travis":
            # make sure we use the time in california 
            today = datetime.datetime.now(tz=pytz.timezone("US/Pacific"))
            todayStr =today.strftime("%m-%d-%Y")
            todayIso =today.strftime("%Y-%m-%d")
            wmap=WorldMap("COVID-19 cases "+todayIso)      
            #wmap.sample()
            wmap.directFromCSV(todayStr,plots=[COVIDCases.CONFIRMED,COVIDCases.DEATHS])
            
    def testCSV(self):
        '''
        test writing a CSV file of all regions
        '''
        gfile = "jhuregions.xml"
        regions=[]
        TinkerPopAble.cache(self.rg, gfile, Region, regions, self.void)  
        isoRegionsByISOCode = {}
        for region in regions:
            if region.isocode is not None:
                isoRegionsByISOCode[region.isocode] = region
        isoRegionList=[v for v in isoRegionsByISOCode.values()];      
        isoRegionList=sorted(isoRegionList, key=lambda region: region.isocode)  
        TinkerPopAble.writeCSV("/tmp/regions.csv",isoRegionList,["isocode","wikiDataId","country","province","lat","lon","pop"])         
        
    def testPMap(self):
        '''
        test creating a map view
        '''
        gfile = "jhuregions.xml"
        regions=[]
        TinkerPopAble.cache(self.rg, gfile, Region, regions, self.void)  
        cases = COVIDCases(regions)
        cases.downloadAll()
        cases.display(False)
        cases.display(True)
        worldmap=PWorldMap("COVID-19 cases "+cases.currentDate)
        #worldmap.sample()
        for casestep in [10,100,1000,10000,100000,1000000]:
            stepmap={}
            for region in cases.regions.values():
                if region.isocode is not None and len(region.isocode)==2 and region.province!="District of Columbia":
                    c=region.total("confirmed")
                    if c>=casestep and c<casestep*10:
                        stepmap[region.isocode.lower()]=c            
            worldmap.wmap.add(">"+str(casestep),stepmap)
        svgfile="/tmp/cases.png"
        worldmap.render(svgfile)
        self.assertTrue(os.path.isfile(svgfile))
        if getpass.getuser()=="wf":
            worldmap.render()    
            
     

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
