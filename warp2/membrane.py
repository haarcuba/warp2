import pickle
import argparse

SECRET = 'eb666635-67d1-49b3-8953-adf018bdf725'

class Server( object ):
    def __init__( self, thing, reader, writer ):
        self._reader = reader
        self._writer = writer
        self._thing = thing
        self._go()

    def _go( self ):
        while True:
            call, args, kwargs = self._read()
            try:
                function = getattr( self._thing, call )
                result = function( * args, ** kwargs )
            except Exception as e:
                result = { SECRET: 1, 'exception': str( e ) }

            self._write( result )

    def _read( self ):
        return pickle.load( self._reader )

    def _write( self, data ):
        pickle.dump( data, self._writer, protocol = 2 )
        self._writer.flush()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( 'code' )
    parser.add_argument( 'reader' )
    parser.add_argument( 'writer' )
    arguments = parser.parse_args()
    exec( arguments.code )
    reader = open( arguments.reader, 'rb' )
    writer = open( arguments.writer, 'wb' )
    try:
        Server( thing, reader, writer )
    except EOFError:
        pass

if __name__ == '__main__':
    main()
