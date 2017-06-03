# Warp 2

Warp 2 wraps Python 2 code and allows access to it by running in in a subprocess.

It communicates with the subprocess using [pickle](https://docs.python.org/3.6/library/pickle.html), so there are limitation to using it - if you need to send unpicklable data, that's a problem.

## Installation

    $ pip install warp2

## Example

here's a Python 2 class of a greeter that tracks a word count:

```python
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
```

here's how to use it from Python 3, note that you must provide a `thing` object for the Warp 2 library to use:

```python
# this is in Python 3
import warp2.warper
import random

greeter = warp2.warper.Warper( 'import greeter ; thing=greeter.Greeter()' )

for _ in range( 10 ):
    greeting = random.choice( [ 'hi', 'hello', "what's up", 'how are you' ] )
    greeter.say( greeting )

print( "summary: " )
print( greeter.counts() )
```

Here's how to run this example from the root of this project (once warp2 is installed of course)

    $ PYTHONPATH=examples/ python examples/three.py 
    what's up
    hello
    how are you
    what's up
    how are you
    hello
    hi
    how are you
    hi
    what's up
    summary: 
    {'how are you': 3, 'hi': 2, 'hello': 2, "what's up": 3}
