#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#======================= END GPL LICENSE BLOCK ========================'

# 1.0.0 - 2022-01-05: Original version
# 1.0.1 - 2022-01-08: Has current objects in scene
# 1.0.2 - 2022-01-19: Selects and activates the imported objects.
# 1.0.3 - 2022-08-07: Misc formatting cleanup before uploading to GitHub.

bl_info = {
    "name": "Light Rig",
    "author": "Jeff Boller",
    "version": (1, 0, 3),
    "blender": (2, 93, 0),
    "location": "View3D > Add > Light > Light Rig",
    "description": "Adds a new three point light rig to the scene",
    "wiki_url": "https://github.com/sundriftproductions/blenderaddon-light-rig/wiki",
    "tracker_url": "https://github.com/sundriftproductions/blenderaddon-light-rig",
    "category": "Lighting",
}

import bpy 
import mathutils 
from mathutils import Vector
import os
from bpy.props import *

def light_rig(self):
    # First, select the outermost layer collection so we import things into predictable places.
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection

    # Load the objects from the external file
    dir = os.path.dirname(os.path.realpath(__file__)) + '/light_rig_PUB.blend/Object/'
    dir = dir.replace("\\", "/")  # Replace all of the backslashes in our path with forward slashes. This will still work on Windows if you don't do this, but this is just to be consistent.
    fp = 'light_rig_PUB.blend'

    self.report({'INFO'}, '  Appending light rig')

    old_objs = set(bpy.context.scene.objects) # Keep track of all of our objects before importing.
    bpy.ops.wm.append(filepath=fp, directory=dir, files=[{'name': 'light_control_panel'}, {'name': 'light-rotate.fill'}, {'name': 'light.fill'}, {'name': 'light-rotate.key'}, {'name': 'light.key'}, {'name': 'light-rotate.rim'}, {'name': 'light.rim'}, {'name': 'light.target'}])

    imported_objs = set(bpy.context.scene.objects) - old_objs # Now figure out which objects we imported...
    for o in imported_objs:
        if o.name.startswith("light_control_panel"):
            # Move the imported object to the cursor.
            o.location.x = bpy.context.scene.cursor.location.x
            o.location.y = bpy.context.scene.cursor.location.y
            o.location.z = bpy.context.scene.cursor.location.z
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
            break

class ThreePointLighting(bpy.types.Operator):
    """Creates a Light Rig"""
    bl_idname = "object.light_rig"
    bl_label = "Light Rig"
    bl_description = "Creates a three point light rig"
    bl_options = {"REGISTER", "UNDO"} 
    
    def execute(self, context):
        light_rig(self)
        return {"FINISHED"} 
    
def add_light_rig(self, context):
    # Check if context is object 
    if context.mode == 'OBJECT':
        # Draws the button in the ui 
        self.layout.operator(
            ThreePointLighting.bl_idname, 
            text = "Light Rig",
            icon = 'LIGHT'
            )

def register():
    bpy.utils.register_class(ThreePointLighting)
    bpy.types.VIEW3D_MT_light_add.append(add_light_rig)

def unregister():
    bpy.utils.unregister_class(ThreePointLighting)
    bpy.types.VIEW3D_MT_light_add.remove(add_light_rig)
  
if __name__ == "__main__":
    register()
