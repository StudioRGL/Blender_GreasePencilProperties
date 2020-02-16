# D.materials[1]['prop'] = 5 # just set 'em, it's pretty simple
# a.line_color[0]
# https://docs.blender.org/api/blender_python_api_2_60_6/bpy.app.handlers.html#persistent-handler-example

import bpy
from enum import Enum

# modules:
# add parameters to all objects (that don't already have them)
# switch viewed paramater
# add controls for parameter switching?


# Ok, yeah globals, sorry
# these two textures are required for the stroke rendering
GPP_STROKE_MAP_FILL_TEXTURE_NAME = 'strokeMap_fillTexture'
GPP_STROKE_MAP_STROKE_TEXTURE_NAME = 'strokeMap_strokeTexture'


def update_func(self, context):
    print("my test function", self)
    updateColorToCurrentMode(self, context)


class GreasePencilCustomProperties(bpy.types.PropertyGroup):
    """Scene properties that are used for the addon"""
    currentMode: bpy.props.IntProperty(update = update_func) = 0 # update = updateColorToCurrentMode
    previousMode: bpy.props.IntProperty() = 0  # so we can see if it changed
    layerNames: bpy.props.StringProperty() = [] # should really be a list but ain't nobody got time for that


class OBJECT_PT_greasePencilCustomPanel(bpy.types.Panel):  
    """ Generates the panel that displays the viewed layer """  
    bl_idname = "OBJECT_PT_greasePencilCustomPanel"
    bl_label = "Grease Pencil Property Layer"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "view_layer" # in ('WINDOW', 'HEADER', 'CHANNELS', 'TEMPORARY', 'UI', 'TOOLS', 'TOOL_PROPS', 'PREVIEW', 'HUD', 'NAVIGATION_BAR', 'EXECUTE', 'FOOTER', 'TOOL_HEADER')
    # bl_category = "View Layer" # "Tool"

    def draw(self, context):
        # You can set the property values that should be used when the user
        # presses the button in the UI.
        props = bpy.context.scene.grease_pencil_custom_properties

        row = self.layout.row()
        row.prop(props, "currentMode", text= "currentMode")
        layerNames = props.layerNames.split()
        currentMode = props.currentMode
        if currentMode<len(layerNames):
            row.label(text=layerNames[currentMode])
        

def hasLength(v):
    """ does it have a length attribute? """
    return ('__len__' in dir(v))


# def addModeProperties():
#    """Adds an enum to the UI that controls the grease pencil display mode"""
#    viewLayers = bpy.context.scene.view_layers.values()
#    for vl in viewLayers:
#        pass#vl['TESTVALUE'] = bpy.props.FloatProperty(name="Test Prob")
#    return


def getAllGreasePencilMaterials():
    """ Returns a list of all grease pencil materials in the scene. """
    answer = []
    for mat in bpy.data.materials:
        if mat.is_grease_pencil:
            answer.append(mat)
    return answer


def setMaterialColor(mat, color):
    """overwrites the material color with the new color. Can give it a single number or a 3 digit"""
    # make sure the color is 3 digit
    if hasLength(color) is False:
        # it has no length attribute, gonna put it in a list
        color = [color, 0, 0]
    elif len(color)<3:
        color += [0, 0, 0]
        color = color[:3]
    # ok now color should be a list of 3 digits

    if mat.grease_pencil.show_fill:
        # set fill
        mat.grease_pencil.fill_color[0] = color[0]
        mat.grease_pencil.fill_color[1] = color[1]
        mat.grease_pencil.fill_color[2] = color[2]
    if mat.grease_pencil.show_stroke:  # note: can do both!
        # set stroke
        mat.grease_pencil.color[0] = color[0]
        mat.grease_pencil.color[1] = color[1]
        mat.grease_pencil.color[2] = color[2]


def getMaterialColor(mat):
    """ returns a 3 float list for RGB """
    # first figure out appropriate value
    if mat.grease_pencil.show_stroke:
        return [mat.grease_pencil.color[0], mat.grease_pencil.color[1], mat.grease_pencil.color[2]]
    elif mat.grease_pencil.show_fill:
        return [mat.grease_pencil.fill_color[0], mat.grease_pencil.fill_color[1], mat.grease_pencil.fill_color[2]]
    return [0, 0, 0]


def updateColorToCurrentMode(self, context):
    """ stores the previous tweaks, set the color from the other thing """
    props = context.scene.grease_pencil_custom_properties
    currentMode = props.currentMode
    previousMode = props.previousMode
    layerNames = props.layerNames.split()

    if currentMode == previousMode:
        return False # didn't need to update
    
    print('switching from mode', layerNames[previousMode], 'to', layerNames[currentMode])


    # note, special case when mode is strokeMap
    # D.materials['stroke_mortar'].grease_pencil.fill_style = 'SOLID'
    # D.materials['stroke_mortar'].grease_pencil.stroke_style = 'TEXTURE'
    # D.materials['stroke_mortar'].grease_pencil.stroke_image = bpy.data.images['horizontalGradient']


    # for all mats
    for mat in getAllGreasePencilMaterials():
        # special case for stroke map
        if layerNames[currentMode] == 'strokeMap':
            mat.grease_pencil.fill_style = 'TEXTURE'
            mat.grease_pencil.stroke_style = 'TEXTURE'
        else:
            # store old value (if it wasn't stroke map)
            if layerNames[previousMode] == 'strokeMap':
                # specific stuff for switching from stroke map
                # turn it solid again
                mat.grease_pencil.fill_style = 'SOLID'
                mat.grease_pencil.stroke_style = 'SOLID'
            else:
                # for all other ones
                color = getMaterialColor(mat)
                storeLocation = mat[layerNames[previousMode]]
                if hasLength(storeLocation):
                    for i in range(len(storeLocation)):
                        if i>=3:
                            break
                        storeLocation[i] = color[i]
                else:
                    mat[layerNames[previousMode]] = color[0] # just set first value

            # load new value
            setMaterialColor(mat, mat[layerNames[currentMode]])

    # update modes
    props.previousMode = currentMode


def addCustomProperty(propertyName, defaultValue):
    """adds a custom property to the list of custom properties, 
    the number of items in the default value list tells it how many channels it should have"""
    scene = bpy.context.scene
    if propertyName not in scene.grease_pencil_custom_properties.layerNames.split():
        scene.grease_pencil_custom_properties.layerNames += ' ' + propertyName

    # for all grease pencil materials
    for mat in getAllGreasePencilMaterials():
        # don't bother if property exists
        if propertyName == 'strokeMap':
            # we don't need to add custom attributes for strokeMap
            # make sure it has the right texture added. Currently textured strokes aren't supported
            mat.grease_pencil.stroke_image = bpy.data.images[GPP_STROKE_MAP_STROKE_TEXTURE_NAME]
            mat.grease_pencil.fill_image = bpy.data.images[GPP_STROKE_MAP_FILL_TEXTURE_NAME]
            mat.grease_pencil.pixel_size = 1000  # magic! shazam
        elif propertyName not in mat.keys():
            # special case for colour
            if propertyName == "param_color":
                defaultValue = getMaterialColor(mat)

            # ok, it doesn't exist, let's add it
            mat[propertyName] = defaultValue
    return


def register():
    """ Required for Blender to recognize this stuff"""
    bpy.utils.register_class(OBJECT_PT_greasePencilCustomPanel)
    bpy.utils.register_class(GreasePencilCustomProperties)
    bpy.types.Scene.grease_pencil_custom_properties = bpy.props.PointerProperty(type=GreasePencilCustomProperties)


def setup():
    """ run this once to set up the system """
    register()

    # check we got the two textures we need:
    for image in [GPP_STROKE_MAP_FILL_TEXTURE_NAME, GPP_STROKE_MAP_STROKE_TEXTURE_NAME]:
        if image not in bpy.data.images:
            raise(Exception('This script requires an image named ' + image + ' to run!'))

    # clear existing layer variables
    props = bpy.context.scene.grease_pencil_custom_properties
    props.layerNames = ''
    # props.currentMode = 0  # don't need to initialize


    # add all the params
    props = [
                ('param_color', [0.5, 0.5, 0.5]),
                ('param_specularSmooth', 0.0),
                ('param_specularRough', 0.0),
                ('strokeMap', 0) # this is a special one, that doesn't create custom attributes
            ]
    for p in props:
        addCustomProperty(p[0], p[1])

    print('completed setup')
    return


# do this thang
setup()



#bpy.app.handlers.depsgraph_update_post.append(updateColorToCurrentMode)