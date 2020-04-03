'''
Created on 22.03.2020

@author: wf
'''
from qwikidata.sparql import return_sparql_query_results
from jhu.loc import Projection
from tp.gremlin import TinkerPopAble

class WikiData:
    @staticmethod
    def stripId(url):
        return url.replace('http://www.wikidata.org/entity/','')
    
    @staticmethod
    def stripLocation(location):
        location=location.replace('Point(','')
        location=location.replace(')','')
        location=location.replace(' ',',')
        return location    
    
class Region(TinkerPopAble):
    '''
    get region info from wikidata
    '''
    regions=[]    
    
    @staticmethod 
    def fromWikiData():
        sparql='''# Find population of COVID regions using the Wikidata Query service
# taken from
# http://wiki.bitplan.com/index.php/SPARQL#PopulationGermanProvinces
# Created 2020-03-22 by Wolfgang Fahl BITPlan GmbH
#
# select the province and it's population
SELECT ?region ?isocc ?isocode4 ?regionLabel ?pop ?location
WHERE 
{
  # any subject
  # which is an instance of
  # https://www.wikidata.org/wiki/Property:P31
  
  # German Bundesland
  # https://www.wikidata.org/wiki/Q1221156
  { ?region wdt:P31 wd:Q1221156. }
  UNION 
  # Province of China 
  { ?region wdt:P31 wd:Q1615742. }
  #  autonomous region of the People's Republic of China (Q57362) 
  UNION 
  { ?region wdt:P31 wd:Q57362. }
  #  special administrative region of China (Q779415) 
  UNION 
  { ?region wdt:P31 wd:Q779415. }  
  # US state
  UNION
  { ?region wdt:P31 wd:Q35657. }
  #  province of Canada (Q11828004) 
  UNION
  { ?region wdt:P31 wd:Q11828004. } 
  #  territory of Canada (Q9357527) 
  UNION
  { ?region wdt:P31 wd:Q9357527. }    
  # Australian state  
  UNION
  { ?region wdt:P31 wd:Q5852411. }
  #  mainland territory of Australia (Q14192234) 
  UNION
  { ?region wdt:P31 wd:Q14192234. }  
  #  autonomous country within the Kingdom of Denmark (Q66724388) 
  UNION
  { ?region wdt:P31 wd:Q66724388. }   
  # country of the Kingdom of the Netherlands (Q15304003) 
  UNION
  { ?region wdt:P31 wd:Q15304003. }   
  #  overseas department of France (Q202216) 
  UNION
  { ?region wdt:P31 wd:Q202216. }       
  #  overseas territory (Q2327385) former top-level subdivision of France applied to certain overseas entities
  UNION
  { ?region wdt:P31 wd:Q2327385. }  
  # Overseas France (Q203396) 
  UNION
  { ?region wdt:P31 wd:Q203396. }
  #  overseas collectivity (Q719487) type of French territorial collectivity, used for several overseas islands or archipelagos
  UNION
  { ?region wdt:P31 wd:Q719487. }     
  # British Overseas Territories (Q46395) 
  UNION
  { ?region wdt:P31 wd:Q46395. }        
  # Crown dependency (Q185086) self-governing possession of the British crown
  UNION
  { ?region wdt:P31 wd:Q185086. }        
  #  administrative territorial entity of a single country (Q15916867) 
  UNION
  { ?region wdt:P31 wd:Q15916867 . }
  #  dependent territory (Q161243) 
  UNION
  { ?region wdt:P31 wd:Q161243 . }  
  #  unitary state (Q179164) 
  UNION
  { ?region wdt:P31 wd:Q179164 . }
  # sovereign state
  UNION 
  { ?region wdt:P31 wd:Q3624078 . }
  # get the population
  # https://www.wikidata.org/wiki/Property:P1082
  OPTIONAL { ?region wdt:P1082 ?pop. }
  # # https://www.wikidata.org/wiki/Property:P297
  OPTIONAL { ?region wdt:P297 ?isocc. }
  # isocode state/province
  OPTIONAL { ?region wdt:P300 ?isocode4. }
  # https://www.wikidata.org/wiki/Property:P625
  OPTIONAL { ?region wdt:P625 ?location. }
  SERVICE wikibase:label {               # ... include the labels
        bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en"
  }
}'''
        res = return_sparql_query_results(sparql)
        for record in (res['results']['bindings']):
            Region.regions.append(Region(record))
            
    def __init__(self, record=None):
        '''
        Constructor
        '''
        if record is None:
            return  
        self.wikiDataId=record['region']['value']
        self.wikiDataId=WikiData.stripId(self.wikiDataId)
        self.name=record['regionLabel']['value']   
        if 'pop' in record:
            self.pop=record['pop']['value']   
        else:    
            self.pop=-1  
        self.isocode="?"
        if 'isocc' in record:
            self.isocode=record['isocc']['value']
        if 'isocode4' in record:
            self.isocode=record['isocode4']['value']
        self.lat=0
        self.lon=0    
        if 'location' in record:    
            self.location=record['location']['value']
            self.location=WikiData.stripLocation(self.location)
            self.lon,self.lat=self.location.split(",")
            self.lon=float(self.lon)
            self.lat=float(self.lat)
            self.coords=Projection.pointToXy(self.location)
        
    @staticmethod
    def ofMap(pMap):
        '''
        create a Region from the given map
        '''
        region=Region()
        region.fromMap(pMap)
        return region        
        
    def __str__(self):
        text= ("%6s;%9s;%40s;%9s;%6.1f;%6.1f" % (self.isocode,self.wikiDataId,self.name,self.pop,self.lat,self.lon))    
        return text
        
            