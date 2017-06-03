import warp2.warper
import random

greeter = warp2.warper.Warper( 'import greeter ; thing=greeter.Greeter()' )

for _ in range( 10 ):
    greeting = random.choice( [ 'hi', 'hello', "what's up", 'how are you' ] )
    greeter.say( greeting )

print( "summary: " )
print( greeter.counts() )
