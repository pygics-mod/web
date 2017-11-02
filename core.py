# -*- coding: utf-8 -*-
'''
Created on 2017. 9. 19.
@author: HyechurnJang
'''

import os
import types
import jzlib
from pygics import export

class Web(jzlib.LifeCycle):
    
    _CACHE_DATA = {}
    
    @classmethod
    def getCache(cls, file_path):
        if file_path in Web._CACHE_DATA: return Web._CACHE_DATA[file_path]
        else:
            class Cache(types.FileType):
                def __init__(self, file_path):
                    with open(file_path, 'rb') as fd: self.data = fd.read()
                    self.file_path = file_path
                @property
                def name(self): return self.file_path
                def read(self): return self.data
                def close(self): return None
            if not os.path.exists(file_path): raise Exception('could not find %s' % file_path)
            cache = Cache(file_path)
            Web._CACHE_DATA[file_path] = cache
            return cache
    
    def __init__(self,
                 url=None,
                 root=None,
                 index=None,
                 cache=True):
        mod_path, mod_name = pmd()
        mod_name = mod_name.replace('.', '/')
        if not url: self.url = '/%s' % mod_name
        elif url[0] == '/': self.url = url
        else: self.url = '/%s/%s' % (mod_name, url)
        if not root: self.root = mod_path
        elif root[0] != '/' : self.root = '%s/%s' % (mod_path, root)
        else: self.root = root
        if index: self._web_index = index
        else: self._web_index = 'index.html'
        self._web_cache = cache
        self._web_cache_data = {}
        
        @export('GET', self.url)
        def get(req, *argv):
            path = '/'.join(argv)
            if path: file_path = '%s/%s' % (self.root, path)
            else: file_path = '%s/%s' % (self.root, self._web_index)
            if self._web_cache: return Web.getCache(file_path)
            else:
                if not os.path.exists(file_path): raise Exception('could not find %s' % path)
                return open(file_path, 'rb')
