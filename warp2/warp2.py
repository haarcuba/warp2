import subprocess
import logging
logging.basicConfig( level = logging.INFO )
import tempfile
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
        self._directory = tempfile.TemporaryDirectory( prefix = 'warp2_' )
        writeFifo = self._makeFifo( 'master_writer' )
        readFifo = self._makeFifo( 'master_reader' )
        self._process = subprocess.Popen(
            [ 'python2', 'warp2/wrapper.py', moduleName, writeFifo, readFifo ], env = env )
        self._writer = open( writeFifo, 'wb' )
        self._reader = open( readFifo, 'rb' )

    def _makeFifo( self, name ):
        fifo = os.path.join( self._directory.name, name )
        logging.info( 'using fifo={}'.format( fifo ) )
        os.mkfifo( fifo )
        return fifo

    def __getattr__( self, name ):
        return _Function( name, self._writer, self._reader )
