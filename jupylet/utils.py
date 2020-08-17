"""
    jupylet/utils.py
    
    Copyright (c) 2020, Nir Aides - nir@winpdb.org

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import functools
import hashlib
import inspect
import pickle
import types
import glm
import os


def abspath(path):

    dirname = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(dirname, path))


def callerpath(levelsup=1):

    ff = inspect.currentframe().f_back
    for i in range(levelsup):
        ff = ff.f_back

    pp = ff.f_globals.get('__file__', '')
    return os.path.dirname(pp)


def auto_read(s):
    return s if '\n' in s else open(s).read()


def o2h(o, n=12):
    return hashlib.sha256(pickle.dumps(o)).hexdigest()[:n]


class Dict(dict):
    
    def __dir__(self):
        return list(self.keys()) + super().__dir__()

    def __getattr__(self, k):
        
        if k not in self:
            raise AttributeError(k)
            
        return self[k]
    
    def __setattr__(self, k, v):
        self[k] = v


def patch_method(obj, key, method):
    
    foo = getattr(obj, key)
    
    if isinstance(foo.__func__, functools.partial):
        return foo
    
    par = functools.partial(method, foo=foo)
    bar = types.MethodType(par, obj)
    bar.__func__.__name__ = foo.__func__.__name__
    
    setattr(obj, key, bar)
    
    return bar


def glm_dumps(o):
    
    if "'glm." not in repr(o.__class__):
        return o
    
    return ('__glm__', o.__class__.__name__, tuple(o))


def glm_loads(o):
    
    if type(o) is not tuple or not o or o[0] != '__glm__':
        return o
    
    return getattr(glm, o[1])(o[2])

    