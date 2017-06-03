# this is in Python 2
import collections

class Greeter( object ):
    def __init__( self ):
        self._counts = collections.defaultdict( lambda: 0 )

    def say( self, what ):
        print what
        self._counts[ what ] += 1
        return 'said: {}'.format( what )

    def counts( self ):
        return dict( self._counts )
