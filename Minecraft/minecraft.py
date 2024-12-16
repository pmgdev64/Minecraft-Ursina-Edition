from ursina import *
from ursinanetworking import *
import keyboard as kb # import keyboard library
# Instantiate ursina here, so that textures can be
# loaded without issue in other modules :)
app = Ursina()

from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar
from mesh_terrain import MeshTerrain
from flake import SnowFall
import random as ra
from bump_system import *
from save_load_system import saveMap, loadMap
from inventory_system import *
from sly import Lexer, Parser

"""
Version 0.1.0 (unlicensed)
[!] this version isn't a copy, clone version of Minecraft 
[!] developed by pmgdev, original by mojang
[!] copyright © 2024-2025 Pmg Foundation. all right reserved.
"""

window.color = color.rgb(0,200,225)
window.title = 'Minecraft'
# indra = Sky()
# indra.color = window.color
subject = FirstPersonController(
    model='assets/player_objects/char.obj',
    textures='assets/player_objects/player/shiroko'
    )
hb1=HealthBar(
    bar_color=color.cyan,
    roundness=.5,
    scale=(1.5, .06)
    )
subject.gravity = 0.0
subject.cursor.visible=True
subject.cursor.color=color.white
subject.height=1.62 # Minecraft eye-level?
subject.camera_pivot.y=subject.height
subject.frog=False # For jumping...
subject.runSpeed=12
subject.walkSpeed=5
subject.blockType=None # Current building mineral.
camera.dash=10 # Rate at which fov changes when running.
camera.fov=origFOV=63
# *** - see inventory_system.py
# window.fullscreen=False

terrain = MeshTerrain(subject,camera)
# snowfall = SnowFall(subject)
# How do you at atmospheric fog?
scene.fog_density=(0,75)
# scene.fog_color=indra.color
scene.fog_color=color.white
generatingTerrain=True

# Generate our terrain 'chunks'.
for i in range(4):
    terrain.genTerrain()
# For loading in a large terrain at start.
# loadMap(subject,terrain)

grass_audio = Audio('step.ogg',autoplay=False,loop=False)
snow_audio = Audio('snowStep.mp3',autoplay=False,loop=False)
grass_audio.volume=0.1

pX = subject.x
pZ = subject.z

class minecraft():
    def launch(self, Args):
        self.Args=Args
        app.run()
    '''
    def chat(self, InputData):
        self.input=str(InputData)
    '''

class Commands(self, Executable):
    command_tokens=[
        'say',
        'execute',
        'kill',
        'title',
        'scoreboard',
        'particle',
        'function',
        'custom_commands'
    ]
    '''
    self.executable=Executable
    def CommandInput(self, DataInput):
        self.datainput=str(DataInput)
    '''

def input(key):
    global generatingTerrain
    terrain.input(key)
    if key=='g':
        generatingTerrain = not generatingTerrain
    # Jumping...
    if key=='space': subject.frog=True
    # Saving and loading...
    if key=='m':
        saveMap(subject.position,terrain.td)
    if key=='l':
        loadMap(subject,terrain)

    if key=='p':
        pause = EditorCamera()

    # Inventory access.
    inv_input(key,subject,mouse)

count=0
earthcounter=0
earthquake_ON=False
sky_textures=load_texture("sky.jpg")
sky_box=Sky(textures=sky_textures)
def update():
    global count, pX, pZ, earthcounter, origFOV

    # Highlight terrain block for mining/building...
    terrain.update()

    # Handle mob ai.
    mob_movement(grey, subject.position, terrain.td)

    count+=1
    if count >= 1:
        
        count=1
        # Generate terrain at current swirl position.
        if generatingTerrain:
            terrain.genTerrain()
            # for i in range(1):
                # terrain.genTerrain()
                
    

    # Change subset position based on subject position.
    if abs(subject.x-pX)>1 or abs(subject.z-pZ)>1:
        pX=subject.x
        pZ=subject.z 
        terrain.swirlEngine.reset(pX,pZ)
        # Sound :)
        if subject.y > 4:
            if snow_audio.playing==False:
                snow_audio.pitch=ra.random()+0.25
                snow_audio.play()
        elif grass_audio.playing==False:
            grass_audio.pitch=ra.random()+0.7
            grass_audio.play()
    
    # *******
    #  Earthquake experiment!
    if earthquake_ON:
        earth_amp=0.1
        earth_freq=0.5
        earthcounter+=earth_freq
        for h in terrain.subsets:
            h.y = (math.sin(terrain.subsets.index(h) + 
                            earthcounter)*earth_amp)#*time.dt
    # *******

    # Walk on solid terrain, and check wall collisions.
    bumpWall(subject,terrain)
    # Running and dash effect.
    if held_keys['shift'] and held_keys['w']:
        subject.speed=subject.runSpeed
        if camera.fov<100:
            camera.fov+=camera.dash*time.dt
    else:
        subject.speed=subject.walkSpeed
        if camera.fov>origFOV:
            camera.fov-=camera.dash*4*time.dt
            if camera.fov<origFOV:camera.fov=origFOV

from mob_system import *

class keyboard_function():
    def camera_mode(camera_mode):
        pass
        
minecraft.launch(Args)
