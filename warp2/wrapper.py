import importlib
import logging
logging.basicConfig( level = logging.INFO )
import sys
import pickle
import argparse

class Server( object ):
    def __init__( self, thing ):
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
        return pickle.load( sys.stdin )

    def _write( self, data ):
        pickle.dump( data, sys.stdout, protocol = 2 )
        sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( 'module' )
    arguments = parser.parse_args()
    moduleName = arguments.module
    module = importlib.import_module( moduleName )
    Server( module )

if __name__ == '__main__':
    main()
