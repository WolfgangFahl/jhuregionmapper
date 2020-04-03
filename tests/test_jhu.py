'''
Created on 2020-03-28

@author: wf
'''
import unittest
import getpass
import os
from pathlib import Path
from tp.gremlin import RemoteGremlin, TinkerPopAble
from jhu.pop import Region
from jhu.jhu import COVIDCases
from jhu.jhu import Region as TRegion
from jhu.loc import Projection

class JohnsHopkinsRegionMappingTest(unittest.TestCase):
    '''
    test mapping johns hopkins covid-19 data province/country region mapping
    via access to a janus graph docker instance using the RemoteGremlin helper class
    '''

    def setUp(self):
        '''
        setUp the environment for the test
        '''
        # default server for janusgraph instance
        self.gremlinserver="localhost"
        # default sharepoint 
        self.sharepoint=str(Path.home())+"/graphdata"
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
        
    def test_CacheRegion(self):
        '''
        test caching region information retrieved from WikiData via a SPARQL query
        '''
        self.clean()
        gfile = "region.xml"
        TinkerPopAble.cache(self.rg, gfile, Region, Region.regions, Region.fromWikiData)  
        # we check the number of regions expected here - please adapt if the
        # SPARQL query or WikiData content changes
        self.assertEquals(424, len(Region.regions))
        self.assertTrue(os.path.isfile(self.rg.sharepoint + gfile))
        pass    
    
    def test_JHU_Regions(self):
        ''' test getting the names from John Hopkins university 
        time series data country and province'''
        cases = COVIDCases()
        cases.downloadAll()
        # for date in ts.dates:
        #    print (date)
        print("%d regions" % len(cases.regions))
        for region in cases.regions.values():
            print ("%35s:%35s %6.1f %6.1f %6d %6d" % (region.country, region.province, region.lat, region.lon,region.total("confirmed"),region.total("deaths")))
            pass
        
    def test_MatchRegions(self):
        '''
        test matching Johns Hopkins University regions to WikiData retrieved Region info by
        lat/lon distance
        '''
        self.clean()
        gfile = "region.xml"
        TinkerPopAble.cache(self.rg, gfile, Region, Region.regions, Region.fromWikiData) 
        print ("cached %3d ISO regions (from WikiData)" % (len(Region.regions)))
        cases = COVIDCases()
        cases.downloadAll()
        print ("loaded %3d case regions (from Johns Hopkins University)" % (len(cases.regions.values())))    
        TRegion.debug = True
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
        regionByWikiDataId = {}
        for iregion in Region.regions:
            regionByWikiDataId[iregion.wikiDataId] = iregion
        for region in cases.regions.values():
            matches = matches + region.matchIsoRegion(regionByWikiDataId, fixes)
        print ("found %3d matches" % (matches))    
            
    def testProjection(self):
        '''
        test the mercator projection
        '''
        point="-0.1285907, 51.50809"
        coords=Projection.pointToXy(point)
        print(coords)
        coords=Projection.wgsToXy(-0.1285907, 51.50809) # longitude first, latitude second.
        print(coords)    


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
