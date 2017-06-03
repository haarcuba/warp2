import subprocess
import pickle
import os

class _Function:
    def __init__( self, name, writer, reader ):
        self._name = name
        self._writer = writer
        self._reader = reader

    def __call__( self, * args, ** kwargs ):
        triplet = self._name, args, kwargs
        pickle.dump( triplet, self._writer, protocol = 2 )
        self._writer.flush()
        response = pickle.load( self._reader )
        return response

class Warp2:
    def __init__( self, moduleName, env = None ):
        input, self._writer = self._pipe()
        self._reader, output = self._pipe()
        self._process = subprocess.Popen( [ 'python2', 'warp2/wrapper.py', moduleName ],
                                          stdin = input,
                                          stdout = output,
                                          env = env )

    def _pipe( self ):
        # r, w = os.pipe2( os.O_NONBLOCK )
        r, w = os.pipe()
        return os.fdopen( r, 'rb' ), os.fdopen( w, 'wb' )

    def __getattr__( self, name ):
        return _Function( name, self._writer, self._reader )
