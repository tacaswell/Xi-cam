"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app --optimize 2 --strip

OS X Notes:

1. Comment out all ...'.__doc__'... lines in pyfits.hdu.table.py AND pyfits.convenience.py
2. Modify inspect:

    def getsourcelines(object):
        '''Return a list of source lines and starting line number for an object.

        The argument may be a module, class, method, function, traceback, frame,
        or code object.  The source code is returned as a list of the lines
        corresponding to the object and the line number indicates where in the
        original source file the first line of code was found.  An IOError is
        raised if the source code cannot be retrieved.'''
        print object
        try: #ADDED by RP
            lines, lnum = findsource(object)

            if ismodule(object): return lines, 0
            else: return getblock(lines[lnum:]), lnum + 1
        except:
            return ['<unkown>',0]

"""
import sys
sys.setrecursionlimit(1500)
from setuptools import setup
from numpy.distutils.core import Extension
import numpy as np
import os
import pygments.styles

#os.environ["CC"] = "gcc"
#os.environ["CXX"] = "g++"

APP = ['main.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True,
           'resources':['gui'],
           'iconfile': 'gui/icon.icns',
           'plist': {
               'CFBundleName': 'HipIES',
               'CFBundleShortVersionString': '1.2.2',  # must be in X.X.X format
               'CFBundleVersion': '1.2.2',
               'CFBundleIdentifier': 'com.lbnl.hipies',  # optional
               'NSHumanReadableCopyright': '@ 2016',  # optional
               'CFBundleDevelopmentRegion': 'English',  #optional - English is default
           },
           'includes': [
               'numpy', 'PySide.QtUiTools.QUiLoader', 'PySide.QtCore', 'PySide.QtGui',
               'PySide.QtXml', 'PIL', 'pipeline.cWarpImage', 'pygments.lexers.python',
               'pygments.styles.monokai', 'pygments.styles.default'
           ],
           'excludes': [
               'matplotlib', 'sympy', 'PyQt4', 'PyQt5', 'pyglet'
           ],
           'packages': ['pipeline', 'daemon', 'hipies', 'PIL', 'nexpy', 'h5py']
}

EXT = Extension(name='pipeline.cWarpImage',
                sources=['cext/cWarpImage.cc', 'cext/remesh.cc'],
                extra_compile_args=[ '-O3', '-ffast-math'],#'-fopenmp',, '-I/opt/local/include'
                #extra_link_args=['-fopenmp'],
                include_dirs=[np.get_include()],

)

setup(
    app=APP,
    options={'py2app': OPTIONS},
    #setup_requires=['py2app'],
    include_dirs=[np.get_include()],
    ext_modules=[EXT],


)

