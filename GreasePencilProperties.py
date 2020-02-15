# D.materials[1]['prop2'] = 5 # just set 'em, it's pretty simple
# a.line_color[0]
# https://docs.blender.org/api/blender_python_api_2_60_6/bpy.app.handlers.html#persistent-handler-example

import bpy
from enum import Enum

# modules:
# add parameters to all objects (that don't already have them)
# switch viewed paramater
# add controls for parameter switching?

class GreasePencilCustomProperties(bpy.types.PropertyGroup):
    """Scene properties that are used for the addon"""
    #camera: bpy.props.StringProperty() = ""
    #panelExpanded_setup: bpy.props.BoolProperty() = True
    #panelExpanded_draw: bpy.props.BoolProperty() = False
    #panelExpanded_solve: bpy.props.BoolProperty() = False
    currentMode: bpy.props.IntProperty() = 0
    previousMode: bpy.props.IntProperty() = 0  # so we can see if it changed
    layerNames: bpy.props.StringProperty() = [] # should really be a list but ain't nobody got time for that
    #customLayers: bpy.props.CollectionProperty() #= [1,2,3]
    #modes: bpy.props.EnumProperty()
    #solve_respectLockedLayers: bpy.props.BoolProperty() = True
    #solve_respectHiddenLayers: bpy.props.BoolProperty() = True


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
        

def addModeProperties():
    """Adds an enum to the UI that controls the grease pencil display mode"""
    viewLayers = bpy.context.scene.view_layers.values()
    for vl in viewLayers:
        pass#vl['TESTVALUE'] = bpy.props.FloatProperty(name="Test Prob")
    return


def getAllGreasePencilMaterials():
    """ Returns a list of all grease pencil materials in the scene. """
    answer = []
    for mat in bpy.data.materials:
        if mat.is_grease_pencil:
            answer.append(mat)
    return answer


def addCustomProperty(propertyName, defaultValue):
    """adds a custom property to the list of custom properties, 
    the number of items in the default value list tells it how many channels it should have"""
    scene = bpy.context.scene
    if propertyName not in scene.grease_pencil_custom_properties.layerNames.split():
        scene.grease_pencil_custom_properties.layerNames += ' ' + propertyName



    # for all grease pencil materials
    for mat in getAllGreasePencilMaterials():
        # don't bother if property exists

        if propertyName not in mat.keys():
            # special case for colour
            if propertyName == "param_color":
                if mat.grease_pencil.show_stroke:
                    defaultValue = [mat.grease_pencil.color[0], mat.grease_pencil.color[1], mat.grease_pencil.color[2]]
                elif mat.grease_pencil.show_fill:
                    defaultValue = [mat.grease_pencil.fill_color[0], mat.grease_pencil.fill_color[1], mat.grease_pencil.fill_color[2]]

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

    # clear existing layer variables
    props = bpy.context.scene.grease_pencil_custom_properties
    props.layerNames = ''
    # props.currentMode = 0  # don't need to initialize


    # add all the params
    props = [
                ('param_color', [0.5, 0.5, 0.5]),
                ('param_specularSmooth', 0),
                ('param_specularRough', 0)
            ]
    for p in props:
        addCustomProperty(p[0], p[1])

    print('completed setup')
    return


setup()

addModeProperties()
