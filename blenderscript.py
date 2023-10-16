import bpy
from math import pi
import os
import numpy
from time import sleep
from random import randint
from random import random
from random import choice
from random import shuffle
from mathutils import Vector

############################################################
def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))

def camera_view_bounds_2d(scene, cam_ob, me_ob):
    """
    Returns camera space bounding box of mesh object.

    Negative 'z' value means the point is behind the camera.

    Takes shift-x/y, lens angle and sensor size into account
    as well as perspective/ortho projections.

    :arg scene: Scene to use for frame size.
    :type scene: :class:`bpy.types.Scene`
    :arg obj: Camera object.
    :type obj: :class:`bpy.types.Object`
    :arg me: Untransformed Mesh.
    :type me: :class:`bpy.types.Mesh´
    :return: a Box object (call its to_tuple() method to get x, y, width and height)
    :rtype: :class:`Box`
    """

    mat = cam_ob.matrix_world.normalized().inverted()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    mesh_eval = me_ob.evaluated_get(depsgraph)
    me = mesh_eval.to_mesh()
    me.transform(me_ob.matrix_world)
    me.transform(mat)

    camera = cam_ob.data
    frame = [-v for v in camera.view_frame(scene=scene)[:3]]
    camera_persp = camera.type != 'ORTHO'

    lx = []
    ly = []

    for v in me.vertices:
        co_local = v.co
        z = -co_local.z

        if camera_persp:
            if z == 0.0:
                lx.append(0.5)
                ly.append(0.5)
            # Does it make any sense to drop these?
            # if z <= 0.0:
            #    continue
            else:
                frame = [(v / (v.z / z)) for v in frame]

        min_x, max_x = frame[1].x, frame[2].x
        min_y, max_y = frame[0].y, frame[1].y

        x = (co_local.x - min_x) / (max_x - min_x)
        y = (co_local.y - min_y) / (max_y - min_y)

        lx.append(x)
        ly.append(y)

    min_x = clamp(min(lx), 0.0, 1.0)
    max_x = clamp(max(lx), 0.0, 1.0)
    min_y = clamp(min(ly), 0.0, 1.0)
    max_y = clamp(max(ly), 0.0, 1.0)

    mesh_eval.to_mesh_clear()

    r = scene.render
    fac = r.resolution_percentage * 0.01
    dim_x = r.resolution_x * fac
    dim_y = r.resolution_y * fac

    # Sanity check
    if round((max_x - min_x) * dim_x) == 0 or round((max_y - min_y) * dim_y) == 0:
        return [0, 0, 0, 0]

    return [
        round(min_x * dim_x),            # X
        round(dim_y - max_y * dim_y),    # Y
        round((max_x - min_x) * dim_x),  # Width
        round((max_y - min_y) * dim_y)   # Height
    ]
        
############################################################

## How to list the objects
# list(bpy.data.objects)

################ The used objects ##########################
# Used Dice Cube = "1"    ------ "Dice" & "Dots"
# Board plane = "Board"
# Background image plane = "Background"
# Light
# Camera

# use metric system
bpy.context.scene.unit_settings.system = "METRIC"
# cube_size = 0.024
# bpy.data.objects['1'].location = (0,0,0.12)
# bpy.data.objects['1'].rotation_euler = (0,3*pi/2,0)
# bpy.data.objects['1'].scale = (cube_size,cube_size,cube_size) # Recommended size: [0.2 - 0.4]
# not necessary to locate and scale the board every time!
# bpy.data.objects['Board'].location = (0,0,0)
# bpy.data.objects['Board'].scale = (0.5,0.5,0.01)
# bpy.data.objects['Camera'].location = (0,0,6)
bpy.data.cameras['Camera'].lens = 5
# bpy.data.objects['Camera'].rotation_euler = (0,0,0)
bpy.data.objects['Light1'].data.use_nodes = True
bpy.data.objects['Light2'].data.use_nodes = True
bpy.data.objects['Light3'].data.use_nodes = True
# bpy.data.objects['Light1'].location = (-10,0,30)
# bpy.data.objects['Light2'].location = (10,0,30)
# bpy.data.objects['Light3'].location = (0,-10,30)
# bpy.data.objects['Light1'].data.node_tree.nodes['Emission'].inputs['Strength'].default_value = 10
# bpy.data.objects['Light2'].data.node_tree.nodes['Emission'].inputs['Strength'].default_value = 10
# bpy.data.objects['Light3'].data.node_tree.nodes['Emission'].inputs['Strength'].default_value = 10

# rendering parameters
filepath = 'C:/Users/shaman/Desktop/projects/blender/setup-production-01/' # output location
# filepath = 'D:/projects/blender/setup-production-01/'
bpy.context.scene.render.engine = "CYCLES"

# RANDOM RESOLUTION
# set the resolution, higher is better and takes more time
resolx = [854, 960, 1024, 1280, 1366] #1600, 1920
resoly = [480, 540, 576, 720, 768] #900, 1080
resoln = ["854x480", "960x540", "1024x576", "1280x720", "1366x786"] #"1600x900", "1920x1080"

# RANDOM SAMPLE #
# set the samples, higher is better and takes more time
samps = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320]
# samps = [320] # test

# prepare dice list and dice
# dice = ["1orange", "1blue", "1green", "1red", "1", "1black"]
dice = ["D2black"]
# EACH DIE SHOULD BE AT THE SAME INITIAL POSITION FOR PROPER NAMING!
# 1 ON Z+, 2 IS X+, 3 IS Y-,
# do not do scaling, bounding box algorithm requires applied transformation
# cube_size = 0.024
# for die in dice:
#    bpy.data.objects[die].scale = (cube_size,cube_size,cube_size) # Recommended size: [0.2 - 0.4]

# prepare renderedimagename and coordinates array
renderednames = []
renderedcoord = []

# RANDOM BACKGROUND IMAGE
# assign images to the board
texfolder = 'C:/Users/shaman/Desktop/projects/blender/wallpapers/'
# texfolder = 'D:/projects/blender/wallpapers/'
texlist = os.listdir(texfolder)

# LIGHT LOCATION TEST    
# assign random location to the lights
# experiment how many different combinations you should and  loop
lights = ["Light1", "Light2", "Light3"]

# RANDOM OBJECTS
# position random objects randomly betweem the camera and the lights
# do not scale
listobjects = ["cylinder", "cube", "simit", "hand1", "mball"]

for procounter in range(50):
    
    # RANDOM RESOLUTION
    # set the resolution, higher is better and takes more time
    randres = randint(0,4)
    bpy.context.scene.render.resolution_x = resolx[randres]
    bpy.context.scene.render.resolution_y = resoly[randres]
    parname = "r" + resoln[randres]
    # default resolutions    
    # bpy.context.scene.render.resolution_x = 1280
    # bpy.context.scene.render.resolution_y = 720


    # RANDOM SAMPLE #
    # set the samples, higher is better and takes more time
    shuffle(samps)
    randsamp = choice(samps)
    bpy.context.scene.cycles.samples = randsamp
    parname = parname + "s" + str(randsamp)
    # default samples
    # bpy.context.scene.cycles.samples = 160

    shuffle(texlist)
    teximg = choice(texlist)
    mat = bpy.data.materials.new(name="New_Mat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    imagepath = texfolder + teximg
    texImage.image = bpy.data.images.load(imagepath)
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
    board =  bpy.data.objects['Board']
    board.active_material = mat
    parname = parname + "b" + teximg[0:7]
    # texfolder = 'D:/projects/blender/textures/'
    # texlist = os.listdir(texfolder)
    # counter = 1
    # for teximg in texlist:
    #    mat = bpy.data.materials.new(name="New_Mat")
    #    mat.use_nodes = True
    #    bsdf = mat.node_tree.nodes["Principled BSDF"]
    #    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    #    imagepath = texfolder + teximg
    #    texImage.image = bpy.data.images.load(imagepath)
    #    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
    #    board =  bpy.data.objects['Board']
    #   board.active_material = mat
        # parname = "backimg" + "img" + str(counter)
        # counter += 1


    # LIGHT LOCATION TEST    
    # assign random location to the lights
    # experiment how many different combinations you should and  loop
    # lights = ["Light1", "Light2", "Light3"]
    #for l in range(10):
    #    for light in lights:
    #        coordxl = -15 + random() * 30
    #        coordyl = -15 + random() * 30
    #        coordzl = 25 + random() * 15
    #        bpy.data.objects[light].location = (coordxl,coordyl,coordzl)
    #    parname = "lloc" + str(l)
    # default locations
    for light in lights:
        coordxl = -15 + random() * 30
        coordyl = -15 + random() * 30
        coordzl = 25 + random() * 15
        bpy.data.objects[light].location = (coordxl,coordyl,coordzl)  


    # RANDOM LIGHT STRENGTH
    # assign random strength to the lights
    # LIGHTS ARE TOO STRONG, REDUCE A BIT!
    # normally 5-25, made 10-25 for colorful dots 
    for light in lights:
        emission = randint(10,25)
        bpy.data.objects[light].data.node_tree.nodes['Emission'].inputs['Strength'].default_value = emission


    # RANDOM CAMERA HEIGHT
    # assign random height to the camera
    # note: camera might be set higher to get a more realistic view
    # note2: experiment with the height for multiple combinations, loop
    # SET HEIGHT GREATER TO ADJUST RESOLUTON!
    camh = 5 + 3 * random()
    bpy.data.objects['Camera'].location = (0,0,camh)          
            
            
    # RANDOM CAMERA ROTATION
    rotx = random() * pi/60
    roty = random() * pi/60
    bpy.data.objects['Camera'].rotation_euler = (rotx,roty,0)
    #    parname = "camrot" + str(rot)
    # default rotation
    # bpy.data.objects['Camera'].rotation_euler = (0,0,0)
         
            
    # RANDOM OBJECTS
    # position random objects randomly betweem the camera and the lights
    # do not scale
    # listobjects = ["cylinder", "cube", "simit", "hand1", "mball"]
    for randobj in listobjects:
        coordobjx = -10 + random() * 20
        coordobjy = -10 + random() * 20
        coordobjz = 10 + random() * 10
        bpy.data.objects[randobj].location = (coordobjx,coordobjy,coordobjz)
        rotatez = random() * 2 * pi
        bpy.data.objects[randobj].rotation_euler = (0,0,rotatez)
    
    
    # RANDOM DIE LOCATION
    # create random x,y coordinates to locate the die
    # do not locate it outside of the view of the camera
    coordx = -3 + random() * 6
    coordy = -2 + random() * 4
    #    parname = "dloc" + str(dl)
    # default
    # coordx = -3 + random() * 6
    # coordy = -1.5 + random() * 3
   
    # dice loop
    for die in dice:
        # set the location of the die
        bpy.data.objects[die].location = (coordx,coordy,0.12) #0.18
        # put unnecessary dice away from the camera
        dieind = dice.index(die)
        undice = dice[:dieind] + dice[dieind+1:]
        dist = 0
        for undie in undice:
            bpy.data.objects[undie].location = (50+dist,50,0)
            dist += 3
        
        rotang = random() * 2 * pi
        # rotation loop
        for i in range(6):
                       
            imageBaseName = die + parname
            
            # EACH DIE SHOULD BE AT THE SAME INITIAL POSITION FOR PROPER NAMING!
            # 1 ON Z+, 2 IS X+, 3 IS Y-
            if i%2 == 0:
                bpy.data.objects[die].rotation_euler = (pi/2,0,rotang)
                if i == 0:
                    imageBaseName = str(5) + "-" + imageBaseName #4
                    renderpath = filepath + "rendered-5/" + imageBaseName
                elif i == 2:
                    imageBaseName = str(6) + "-" + imageBaseName
                    renderpath = filepath + "rendered-6/" + imageBaseName
                else:
                    imageBaseName = str(3) + "-" + imageBaseName #2
                    renderpath = filepath + "rendered-3/" + imageBaseName
            else:
                bpy.data.objects[die].rotation_euler = (0,pi/2,rotang)
                if i == 1:
                    imageBaseName = str(4) + "-" + imageBaseName #5
                    renderpath = filepath + "rendered-4/" + imageBaseName
                elif i == 3:
                    imageBaseName = str(2) + "-" + imageBaseName #3
                    renderpath = filepath + "rendered-2/" + imageBaseName
                else:
                    imageBaseName = str(1) + "-" + imageBaseName
                    renderpath = filepath + "rendered-1/" + imageBaseName
                    
            # RANDOM ROTATION
            # bpy.data.objects[die].rotation_euler = (0,0,rotang)
            
            # apply transformation
            obj = bpy.context.scene.objects.get(die)
            if obj: obj.select_set(True)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                
            # the origin of the object may shift due to transformation, reset
            obj = bpy.context.scene.objects.get(die)
            if obj: obj.select_set(True)
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
            
            # run bounding box algorithm and save the coordinates
            rencoords = camera_view_bounds_2d(bpy.context.scene, bpy.context.scene.camera, bpy.data.objects.get(die))
            renderedcoord.append(rencoords)
            # run render operation and output results
            bpy.context.scene.render.filepath = renderpath
            renderednames.append(bpy.context.scene.render.filepath)
            bpy.ops.render.render(write_still=True)
            
            # RESET THE ROTATION
            bpy.data.objects[die].rotation_euler = (0,0,-rotang)
            # apply transformation
            obj = bpy.context.scene.objects.get(die)
            if obj: obj.select_set(True)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            # the origin of the object may shift due to transformation, reset
            obj = bpy.context.scene.objects.get(die)
            if obj: obj.select_set(True)
            bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
            
            # REST THE GPU
            sleep(1)

# output coordinates and rendered image names
with open(filepath + 'names024.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % name for name in renderednames)
with open(filepath + 'coords024.txt', 'w') as filehandle:
    filehandle.writelines("%s\n" % coord for coord in renderedcoord)

## Change the location
# bpy.data.objects['1'].location = (0,0,0.2)
# bpy.data.objects['Camera'].location = (0,0,9)
# bpy.data.objects['Board'].location = (-5,-4,10)

## Rotate the object
# bpy.data.objects['1'].rotation_euler = (0,0,0)
# bpy.data.objects['1'].rotation_euler = (pi/2,0,0)
# bpy.data.objects['Camera'].rotation_euler = (0,0,pi/2)
# bpy.data.cameras['Camera'].lens = 5

## Resize the object
# bpy.data.objects['1'].scale = (0.2,0.2,0.2) # Recommended size: [0.2 - 0.4]
# bpy.data.objects['Board'].scale = (7,8,0.01)
# bpy.data.objects['Background'].scale = (7,8,0.01)
