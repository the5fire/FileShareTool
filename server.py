#_*_encoding=utf-8_*_

from xmlrpclib import ServerProxy,Fault
from os.path import join, abspath,isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
import sys
import xmlrpclib

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED = 100
ACCESS_DENIED = 200

class UnhandledQuery(Fault):
    '''
    that's show can't handle the query exception
    '''
    def __init__(self,message="Couldn't handle the query"):
        Fault.__init__(self, UNHANDLED, message)
        
class AccessDenied(Fault):
    '''
    when user try to access the forbiden resources raise exception
    '''
    def __init__(self, message="Access denied"):
        Fault.__init__(self, ACCESS_DENIED, message)
        
def inside(dir,name):
    '''
    check the dir that user defined is contain the filename the user given
    '''
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir,''))
def getPort(url):
    '''
    get the port num from the url
    '''
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])
        
class Node:
    
    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname = dirname
        self.secret = secret
        self.known = set()
        
    def query(self, query, history = []):
        try:
            return self._handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            if len(history) > MAX_HISTORY_LENGTH: raise
            return self._broadcast(query,history)
            
    def hello(self,other):
        self.known.add(other)
        return 0
    def fetch(self, query, secret):
        
        if secret != self.secret: raise
        result = self.query(query)
        f = open(join(self.dirname, query),'w')
        f.write(result.data)
        f.close()
        return 0

    def remoteList(self, remote_url):
	#print 'get remotelist'
	s = ServerProxy(remote_url)
	return s.list()

    def _start(self):
        s = SimpleXMLRPCServer(("",getPort(self.url)),logRequests=False)
        s.register_instance(self)
        s.serve_forever()

    
    def _handle(self, query):
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name):raise UnhandledQuery
        if not inside(dir,name):raise AccessDenied
        return xmlrpclib.Binary(open(name).read())
        
    def _broadcast(self, query, history):
        
        for other in self.known.copy():
            if other in history: continue
            try:
                s = ServerProxy(other)
                return s.query(query, history)
            except Fault, f:
                if f.faultCode == UNHANDLED:pass
                else: self.known.remove(other)
            except:
                self.known.remove(other)
                
        raise UnhandledQuery
