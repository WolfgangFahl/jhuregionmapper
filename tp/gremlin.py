'''
Created on 2020-03-30

@author: wf
'''
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph
from shutil import copyfile
import os

class RemoteGremlin(object):
    '''
    helper for remote gremlin connections
    '''

    def __init__(self, server, port=8182):
        '''
        construct me with the given server and port
        '''
        self.server=server
        self.port=port    
        
    def sharepoint(self,sharepoint,sharepath):
        '''
        set up the sharepoint
        '''
        self.sharepoint=sharepoint
        self.sharepath=sharepath
        
        
    def share(self,file):
        '''
        share the given file  and return the path as seen by the server
        '''
        fbase=os.path.basename(file)
        copyfile(file,self.sharepoint+fbase)
        return self.sharepath+fbase
            
    def open(self):
        '''
        open the remote connection
        '''
        self.graph = Graph()
        self.url='ws://%s:%s/gremlin' % (self.server,self.port)
        self.connection = DriverRemoteConnection(self.url, 'g')    
        # The connection should be closed on shut down to close open connections with connection.close()
        self.g = self.graph.traversal().withRemote(self.connection)

    def close(self):
        '''
        close the remote connection
        '''
        self.connection.close()    
        
class TinkerPopAble(object):
    '''
    mixing for classes to store and retrieve from python
    '''
    debug=False
    
    def toVertex(self,g):
        '''
        create a vertex from me
        '''
        label=type(self).__name__;
        t=g.addV(label)
        if TinkerPopAble.debug:
            print(label)
        for name,value in vars(self).items():
            if TinkerPopAble.debug:
                print("\t%s=%s" % (name,value))
            t=t.property(name,value)
        t.iterate()    
        
    def fromMap(self,pMap):
        '''
        fill my attributes from the given pMap dict
        '''
        for name,value in pMap.items():
            self.__setattr__(name, value[0])    
            
    @staticmethod        
    def cache(rg,gfile,clazz,objectList,initFunction):
        '''
        generic save
        '''
        g=rg.g
        clazzname=clazz.__name__
        if os.path.isfile(rg.sharepoint+gfile):
            g.io(rg.sharepath+gfile).read().iterate()
            for pMap in g.V().hasLabel(clazzname).valueMap().toList():
                if TinkerPopAble.debug:
                    print (pMap)
                instance=clazz.ofMap(pMap)
                objectList.append(instance)
                if TinkerPopAble.debug:
                    print (instance)
        else:
            initFunction()
            for instance in objectList:
                if TinkerPopAble.debug:
                    print(instance)
                instance.toVertex(g)
            g.io(rg.sharepath+gfile).write().iterate()    
        pass        
    