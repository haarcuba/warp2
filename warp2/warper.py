import subprocess
import tempfile
import pickle
import os

SECRET = 'eb666635-67d1-49b3-8953-adf018bdf725'

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
        if type(response) is dict:
            if SECRET in response:
                raise Exception( response[ 'exception' ] )
        return response

class Warper:
    def __init__( self, moduleName, env = None, python2 = 'python2' ):
        HERE = os.path.dirname( __file__ )
        MEMBRANE = os.path.join( HERE, 'membrane.py' )
        self._directory = tempfile.TemporaryDirectory( prefix = 'warp2_' )
        writeFifo = self._makeFifo( 'master_writer' )
        readFifo = self._makeFifo( 'master_reader' )
        self._process = subprocess.Popen( [ python2, MEMBRANE, moduleName, writeFifo, readFifo ], env = env )
        self._writer = open( writeFifo, 'wb' )
        self._reader = open( readFifo, 'rb' )

    def _makeFifo( self, name ):
        fifo = os.path.join( self._directory.name, name )
        os.mkfifo( fifo )
        return fifo

    def __getattr__( self, name ):
        return _Function( name, self._writer, self._reader )
