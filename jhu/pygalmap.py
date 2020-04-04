'''
Created on 2020-04-04

@author: wf
'''
from pygal_maps_world.maps import World


class PWorldMap(object):
    '''
    classdocs
    '''


    def __init__(self,title):
        '''
        Constructor
        '''
        self.wmap =World()
        self.wmap.title=title
        
    def sample(self):
        self.wmap.add('F countries', ['fr', 'fi'])
        self.wmap.add('M countries', ['ma', 'mc', 'md', 'me', 'mg',
                                           'mk', 'ml', 'mm', 'mn', 'mo',
                                           'mr', 'mt', 'mu', 'mv', 'mw',
                                           'mx', 'my', 'mz'])
        self.wmap.add('U countries', ['ua', 'ug', 'us', 'uy', 'uz'])    
        self.wmap.add('North America',{'ca': 84949494949,'mx': 494794164,'us': 99794616})
        
    def render(self,filename=None):    
        '''
        render the map
        see http://www.pygal.org/en/stable/documentation/output.html
        '''
        if filename is None:
            self.wmap.render_in_browser()
        else:
            if filename.endswith(".png"):
                self.wmap.render_to_png(filename)
            else:    
                self.wmap.render_to_file(filename)
        