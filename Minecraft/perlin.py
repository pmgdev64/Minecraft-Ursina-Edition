from perlin_module import PerlinNoise
from math import sin
from ursina import Text, destroy

class Perlin:
    def __init__(this):
        # this.seed=randint(0,1000000)
        this.seed=-9337280445
        world=Text("Loaded Seed: "+str(this.seed)",scale=3)
        # Destroy the text on screen after 10 seconds.
        destroy(world,10)

        # this.seed = ord('y')+ord('o')
        # Original values.
        this.octaves = 8
        this.freq = 256
        this.amp = 18    

        this.pNoise_continental = PerlinNoise( seed=this.seed,
                                    octaves=1)

        this.pNoise_details = PerlinNoise(  seed=this.seed,
                                    octaves=this.octaves)
        

    def getHeight(this,x,z):
        y = 0
        y = this.pNoise_continental([x/512,z/512])*128
        y += this.pNoise_details([x/this.freq,z/this.freq])*this.amp
        
        # Apply some predictable surface variation.
        sAmp=0.33
        y+=sin(z)*sAmp
        y+=sin(x*0.5)*sAmp
        return y
