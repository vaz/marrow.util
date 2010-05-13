# encoding: utf-8


"""Compatability features.

Python 2.5 is the minimum version supported by Pulp, and great effort is being made to support Python 3.x.
"""

from __future__ import with_statement
import sys, traceback

import pulp.util.bunch


__all__ = ['execfile', 'exception', 'binary', 'unicode', 'IO', 'parse_qsl']



if sys.version_info >= (3,0): # pragma: no cover
    def execfile(filename, globals_=None, locals_=None):
        if globals_ is None:
            globals_ = globals()
        
        if locals_ is None:
            locals_ = globals_
        
        exec(compile(open(filename).read(), filename, 'exec'), globals_, locals_)

else:
    from __builtin__ import execfile


def exception(maxTBlevel=None):
    """Retrieve useful information about an exception.
    
    Returns a bunch (attribute-access dict) with the following information:
    
    * name: exception class name
    * cls: the exception class
    * exception: the exception instance
    * trace: the traceback instance
    * formatted: formatted traceback
    * args: arguments to the exception instance
    
    This functionality allows you to trap an exception in a method agnostic to differences between Python 2.x and 3.x.
    """
    
    cls, exc, trbk = sys.exc_info()
    excName = cls.__name__
    excArgs = getattr(exc, 'args', None)
    excTb = traceback.format_tb(trbk, maxTBlevel)
    
    return pulp.util.bunch.Bunch(
            name = excName,
            cls = cls,
            exception = exc,
            trace = trbk,
            formatted = excTb,
            args = excArgs
        )    


# Binary and Unicode representations for Python 2.5, 2.6+, or 3.x.
if sys.version_info >= (2, 6) and sys.version_info < (3, 0):
    binary = bytes
    unicode = unicode

elif sys.version_info >= (3, 0): # pragma: no cover
    binary = bytes
    unicode = str

else: # pragma: no cover
    binary = str
    unicode = unicode


# In-memory binary stream representation for Python 2.5 or 2.6+.
# Query string parsing.
if sys.version_info >= (2, 6):
    from io import BytesIO as IO
    from urlparse import parse_qsl
    
else: # pragma: no cover
    try:
        from cStringIO import cStringIO as IO
        
    except ImportError:
        from StringIO import StringIO as IO
    
    from cgi import parse_qsl
