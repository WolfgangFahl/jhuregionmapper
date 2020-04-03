'''
Created on 2020-03-28

@author: wf
'''
import unittest
import os
from tp.gremlin import RemoteGremlin, TinkerPopAble
from jhu.pop import Region
from jhu.jhu import TimeSeries
from jhu.jhu import Region as TRegion
from jhu.loc import Projection


class JanusGraphTest(unittest.TestCase):
    '''
    test access to a janus graph docker instance via the RemoteGremlin helper class
    '''

    def setUp(self):
        self.rg = RemoteGremlin("capri.bitplan.com")
        self.rg.open()
        self.rg.sharepoint("/Volumes/bitplan/user/wf/graphdata/", "/graphdata/")
        pass

    def tearDown(self):
        self.rg.close()
        pass
    
    def clean(self):
        # get the vertices
        gV = self.rg.g.V()
        # drop the existing content of the graph
        gV.V().drop().iterate()
    
    def testJanusGraph(self):
        self.clean()
        # we have a traversal now
        # assert isinstance(gV,GraphTraversal)
        # convert it to a list to get the actual vertices
        vList = self.rg.g.V().toList()
        print (len(vList))
        assert len(vList) == 0
        pass
    
    def test_saveGraph(self):
        self.clean()
        g = self.rg.g
        g.addV("country").property("name", "Germany").iterate()
        gfile = "countries.xml"
        g.io(self.rg.sharepath + gfile).write().iterate()
        self.assertTrue(os.path.isfile(self.rg.sharepoint + gfile))
        
    def test_CacheRegion(self):
        '''
        test caching region information
        '''
        self.clean()
        gfile = "region.xml"
        TinkerPopAble.cache(self.rg, gfile, Region, Region.regions, Region.fromWikiData)  
        self.assertEquals(415, len(Region.regions))
        self.assertTrue(os.path.isfile(self.rg.sharepoint + gfile))
        pass    
    
    def test_JHU_Regions(self):
        ''' test the names from John Hopkins university time series data '''
        ts = TimeSeries()
        # for date in ts.dates:
        #    print (date)
        print("%d regions" % len(ts.regions))
        for region in ts.regions:
            print ("%s:%s %4.1f %4.1f" % (region.country, region.province, region.lat, region.lon))
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
        ts = TimeSeries()
        print ("loaded %3d case regions (from Johns Hopkins University)" % (len(ts.regions)))    
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
        # political incorrect ?
                 "Kosovo;":"Q403","West Bank and Gaza;":"Q801",
        # exotic case Cruise ship with lat/lon - in Oakland California ...
                 "Canada;Grand Princess":"Q99"
        }
        regionByWikiDataId = {}
        for iregion in Region.regions:
            regionByWikiDataId[iregion.wikiDataId] = iregion
        for region in ts.regions:
            matches = matches + region.matchIsoRegion(regionByWikiDataId, fixes)
        print ("found %3d matches" % (matches))    
            
    def test_loadGraph(self):
        self.clean()
        g = self.rg.g
        graphmlFile = "air-routes-small.xml";
        shared = self.rg.share(graphmlFile)
        # read the content from the air routes example
        g.io(shared).read().iterate()
        vCount = g.V().count().next()
        print ("%s has %d vertices" % (shared, vCount))
        assert vCount == 47
        
    def testProjection(self):
        point="-0.1285907, 51.50809"
        coords=Projection.pointToXy(point)
        print(coords)
        coords=Projection.wgsToXy(-0.1285907, 51.50809) # longitude first, latitude second.
        print(coords)    


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
