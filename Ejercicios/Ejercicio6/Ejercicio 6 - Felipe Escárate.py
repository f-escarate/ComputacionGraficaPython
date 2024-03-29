# coding=utf-8
"""Ejercicio 6 - Felipe Escárate"""

import glfw
from OpenGL.GL import *
import numpy as np
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath
from curves import *

__author__ = "Daniel Calderon"
__license__ = "MIT"

############################################################################

def createColorPyramid(r, g ,b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions         colors
        -0.5, 0.5,  0,  r, g, b,
         0.5, -0.5, 0,  r, g, b,
         0.5, 0.5,  0,  r, g, b,
        -0.5, -0.5, 0,  r, g, b,
         0, 0,  0.5,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         0, 1, 3,
         0, 2, 4,
         2, 4, 1,
         3, 4, 1,
         0, 4, 3]

    return bs.Shape(vertices, indices)

def create_lake():
    return

def create_tree(pipeline):
    # Piramide verde
    green_pyramid = createColorPyramid(0, 1, 0)
    gpuGreenPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGreenPyramid)
    gpuGreenPyramid.fillBuffers(green_pyramid.vertices, green_pyramid.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_quad = bs.createColorCube(139/255, 69/255, 19/255)
    gpuBrownQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownQuad)
    gpuBrownQuad.fillBuffers(brown_quad.vertices, brown_quad.indices, GL_STATIC_DRAW)

    # Tronco
    tronco = sg.SceneGraphNode("tronco")
    tronco.transform = tr.scale(0.05, 0.05, 0.2)
    tronco.childs += [gpuBrownQuad]

    # Hojas
    hojas = sg.SceneGraphNode("hojas")
    hojas.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.uniformScale(0.25)])
    hojas.childs += [gpuGreenPyramid]

    # Arbol
    tree = sg.SceneGraphNode("arbol")
    tree.transform = tr.identity()
    tree.childs += [tronco, hojas]

    return tree


def create_house(pipeline):
    # Piramide cafe
    brown_pyramid = createColorPyramid(166/255, 112/255, 49/255)
    gpuBrownPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownPyramid)
    gpuBrownPyramid.fillBuffers(brown_pyramid.vertices, brown_pyramid.indices, GL_STATIC_DRAW)

    # Cubo rojo
    red_cube = bs.createColorCube(1, 0, 0)
    gpuRedCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRedCube)
    gpuRedCube.fillBuffers(red_cube.vertices, red_cube.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_cube = bs.createColorCube(166/255, 112/255, 49/255)
    gpuBrownCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownCube)
    gpuBrownCube.fillBuffers(brown_cube.vertices, brown_cube.indices, GL_STATIC_DRAW)

    # Techo
    techo = sg.SceneGraphNode("techo")
    techo.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.scale(0.2, 0.4, 0.2)])
    techo.childs += [gpuBrownPyramid]

    # Base
    base = sg.SceneGraphNode("base")
    base.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.2, 0.4, 0.2)])
    base.childs += [gpuRedCube]

    # Puerta
    puerta = sg.SceneGraphNode("puerta")
    puerta.transform = tr.matmul([tr.translate(0, -0.2, 0), tr.scale(0.05, 0.001, 0.1)])
    puerta.childs += [gpuBrownCube]

    # Casa
    casa = sg.SceneGraphNode("house")
    casa.transform = tr.identity()
    casa.childs += [techo, base, puerta]

    return casa

def create_skybox(pipeline):
    shapeSky = bs.createTextureCube('paisaje.jfif')
    gpuSky = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuSky)
    gpuSky.fillBuffers(shapeSky.vertices, shapeSky.indices, GL_STATIC_DRAW)
    gpuSky.texture = es.textureSimpleSetup(
        getAssetPath("paisaje2.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    skybox = sg.SceneGraphNode("skybox")
    skybox.transform = tr.matmul([tr.translate(0, 0, 0.3), tr.uniformScale(2)])
    skybox.childs += [gpuSky]

    return skybox

def create_floor(pipeline):
    shapeFloor = bs.createTextureQuad(8, 8)
    gpuFloor = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuFloor)
    gpuFloor.texture = es.textureSimpleSetup(
        getAssetPath("grass.jfif"), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    gpuFloor.fillBuffers(shapeFloor.vertices, shapeFloor.indices, GL_STATIC_DRAW)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(2, 2, 1)])
    floor.childs += [gpuFloor]

    return floor

def createBoat(pipeline):
    # Cubo cafe
    boat = bs.createColorCube(166/255, 112/255, 49/255)
    gpuBoat = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBoat)
    gpuBoat.fillBuffers(boat.vertices, boat.indices, GL_STATIC_DRAW)

    boatNode = sg.SceneGraphNode("floor")
    boatNode.childs += [gpuBoat]
    return boatNode

def create_lake():
    curve1 = catmullRomSpline
    curve2 = catmullRomSpline2


    vertices = [
        curve1[0][0], curve1[0][1], curve1[0][2], 0.0, 1.0, 1.0,
        curve2[0][0], curve2[0][1], curve2[0][2], 0.0, 1.0, 1.0,]

    indices =[]
    
    for i in range(len(curve1)-1):
        if i%2 == 0:
            curva = curve1
        else:
            curva = curve2
        vertices += [
            curva[i][0], curva[i][1], curva[i][2], 0.0, 1.0, 1.0,]
        indices += [i,i+1,i+2]

    return bs.Shape(vertices, indices)

def create_lakeNode(pipeline):
    lake = create_lake()
    gpuLake = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuLake)
    gpuLake.fillBuffers(lake.vertices, lake.indices, GL_STATIC_DRAW)

    lakeNode = sg.SceneGraphNode("lake")
    lakeNode.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(1, 1, 1)])
    lakeNode.childs += [gpuLake]

    return lakeNode

def create_decorations(pipeline):
    lake = create_lakeNode(pipeline)
    lake.transform = tr.translate(-0.9, 0, 0)

    boat = createBoat(pipeline)
    boat.transform = tr.matmul([tr.translate(-1.0,0,0),tr.scale(0.1, 0.05, 0.05)])

    boatMovement = sg.SceneGraphNode("boat")
    boatMovement.transform = tr.identity()
    boatMovement.childs = [boat]

    tree1 = create_tree(pipeline)
    tree1.transform = tr.translate(0.5, 0, 0)

    tree2 = create_tree(pipeline)
    tree2.transform = tr.translate(-0.5, 0, 0)

    tree3 = create_tree(pipeline)
    tree3.transform = tr.translate(0, -0.5, 0)

    tree4 = create_tree(pipeline)
    tree4.transform = tr.translate(-0.2, 0.5, 0)

    tree5 = create_tree(pipeline)
    tree5.transform = tr.translate(0.2, 0.5, 0)

    house = create_house(pipeline)
    house.transform = tr.translate(0, 0.5, 0)

    decorations = sg.SceneGraphNode("decorations")
    decorations.transform = tr.identity()
    decorations.childs += [tree1, tree2, tree3, tree4, tree5, house, lake, boatMovement]    

    return decorations




############################################################################

# A class to store the application control
class Controller:
    def __init__(self):
        self.fillPolygon = True
###########################################################
        self.theta = np.pi
        self.eye = [0, 0, 0.1]
        self.at = [0, 1, 0.1]
        self.up = [0, 0, 1]
        self.index = 0
        self.boat = 0
        self.boatdirection = 1
###########################################################


# global controller as communication with the callback function
controller = Controller()

def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS and action != glfw.REPEAT:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)
    
###########################################################

    elif key == glfw.KEY_W:
        controller.eye += (controller.at - controller.eye) * controller.index
        controller.at += (controller.at - controller.eye) * controller.index
    elif key == glfw.KEY_S:
        controller.eye -= (controller.at - controller.eye) * controller.index
        controller.at -= (controller.at - controller.eye) * controller.index
    elif key == glfw.KEY_D:
        controller.theta -= controller.index*np.pi
    elif key == glfw.KEY_A:
        controller.theta += controller.index*np.pi
    
    elif key == glfw.KEY_H:
        controller.boat += controller.boatdirection

    else:
        print('Unknown key')
    
    if controller.boat==len(catmullRomSplineBoat)-1:
        controller.boatdirection = -1
    if controller.boat==0:
        controller.boatdirection = 1

###########################################################


if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(window, True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Ejercicio 6 - Felipe Escárate", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)

    # Creating shader programs for textures and for colors
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()
    colorShaderProgram = es.SimpleModelViewProjectionShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)

###########################################################################################
    # Creating shapes on GPU memory

    decorations = create_decorations(colorShaderProgram)
    skybox = create_skybox(textureShaderProgram)
    floor = create_floor(textureShaderProgram)

###########################################################################################

    # View and projection
    projection = tr.perspective(60, float(width)/float(height), 0.1, 100)

    t0 = glfw.get_time()
    i = controller.boat
    while not glfw.window_should_close(window):
        t1 = glfw.get_time()
        controller.index = (t1 - t0)*10
        t0 = t1
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

###########################################################################

        at_x = controller.eye[0] + np.cos(controller.theta)
        at_y = controller.eye[1] + np.sin(controller.theta)
        controller.at = np.array([at_x, at_y, controller.at[2]])

        view = tr.lookAt(controller.eye, controller.at, controller.up)

###########################################################################

        ############################
        i = controller.boat
        movimientoBote = sg.findNode(decorations, "boat")
        movimientoBote.transform = tr.translate(catmullRomSplineBoat[i][0], catmullRomSplineBoat[i][1], catmullRomSplineBoat[i][2])

        ################################

        # Drawing (no texture)
        glUseProgram(colorShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        #glUniformMatrix4fv(glGetUniformLocation(colorShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(decorations, colorShaderProgram, "model")
        
        

        # Drawing dice (with texture, another shader program)
        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        #glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "model"), 1, GL_TRUE, tr.identity())

        sg.drawSceneGraphNode(skybox, textureShaderProgram, "model")
        sg.drawSceneGraphNode(floor, textureShaderProgram, "model")       

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()
