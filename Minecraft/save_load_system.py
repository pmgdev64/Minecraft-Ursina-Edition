"""
Saving and loading a terrain 'map'.
"""
import os, sys, pickle
from ursina import Text, destroy

mapName='saves/june_test_1.land'

def saveMap(_subPos, _td):
    # Open main module directory for correct file.
    path = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(path)
    savemap=Text(text='saved map name: '+map_data, scale=0.5)
    destroy(savemap, 6) #delete the text after 6sec when the world is saved.             

    with open(mapName, 'wb') as f:

        map_data = [_subPos, _td]

        pickle.dump(map_data, f)

        map_data.clear()

class WorldNotFound(Exception):
    def __init__(self, msg):
        self.msg=msg
        print('World Not Loaded.\nFinished At Exit Code 1')

def loadMap(_subject,_terrain):
    if os.path.isfile(mapName):
        # Open main module directory for correct file.
        path = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(path)
        with open(mapName, 'rb') as f:
            map_data = pickle.load(f)

        loadmap=Text(text='loaded map name: '+map_data, scale=0.5)
        destroy(loadmap, 6) #delete the text after 6sec when the world is loaded (Looks Like savemap).             
                 

        # Empty out current terrain objects.
        for s in _terrain.subsets:
            destroy(s)
        _terrain.td={}
        _terrain.vd={}
        _terrain.subsets=[]
        _terrain.setup_subsets()
        _terrain.currentSubset=1
        # Without copy?
        _terrain.td=map_data[1]
        # Iterate over terrain dictionary and
        # if we find 't' then generate a block.
        # Note this means we'll lose colour info etc.
        i = 0 # Which subset to build block on?
        for key in _terrain.td:
            whatT=_terrain.td.get(key)
            if whatT!=None and whatT!='g':
                x = key[0]
                y = key[1]
                z = key[2]
                if i>=len(_terrain.subsets)-1:
                    i=0
                _terrain.genBlock(x,y,z,subset=i,gap=False,blockType=whatT)
                i+=1

        # And reposition subject according to saved map.
        _subject.position=map_data[0]
        # Reset swirl engine.
        _terrain.swirlEngine.reset( _subject.position.x,
                                _subject.position.z)
        # Regenerate subset models, so that we can see terrain.
        for s in _terrain.subsets:
            s.model.generate()

    if not os.path.isfile(mapName):
        raise WorldNotFound('Cannot Load Map Name:', mapName)
