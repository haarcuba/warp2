import importlib
import logging
logging.basicConfig( level = logging.INFO )
import sys
import pickle
import argparse

class Server( object ):
    def __init__( self, thing, reader, writer ):
        self._reader = reader
        self._writer = writer
        self._thing = thing
        self._go()

    def _go( self ):
        while True:
            call, args, kwargs = self._read()
            logging.info( 'read {}'.format( ( call, args, kwargs ) ) )
            function = getattr( self._thing, call )
            result = function( * args, ** kwargs )
            logging.info( 'write {}'.format( result ) )
            self._write( result )

    def _read( self ):
        return pickle.load( self._reader )

    def _write( self, data ):
        pickle.dump( data, self._writer, protocol = 2 )
        self._writer.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( 'module' )
    parser.add_argument( 'reader' )
    parser.add_argument( 'writer' )
    arguments = parser.parse_args()
    moduleName = arguments.module
    module = importlib.import_module( moduleName )
    reader = open( arguments.reader, 'rb' )
    writer = open( arguments.writer, 'wb' )
    Server( module, reader, writer )

if __name__ == '__main__':
    main()
