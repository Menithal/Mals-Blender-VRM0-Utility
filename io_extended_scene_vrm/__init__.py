# ##### BEGIN GPL LICENSE BLOCK #####
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
# ##### END GPL LICENSE BLOCK #####
# Copyright 2023 Matti 'Menithal' Lahtinen
import bpy
from .ext.przemir.apply_modifier_for_object_with_shapekeys.ApplyModifierForObjectWithShapeKeys import ApplyModifierForObjectWithShapeKeysOperator
from .utility import blender_copy_re, operator_exists
from .ui import armature, shapekeys

bl_info = {
    "name": "Mals' Extended VRM",
    "author": " 'Menithal' ", 
    "version": (0, 0, 1 ),
    "blender": (3, 0, 0),
    "location": "Pose Mode",
    "description": "Additional VRM Tools",
    "warning": "",
    "wiki_url": "",
    "support": "COMMUNITY",
    "category": "Addon Extension",
}

# classes = () 

# module_register, module_unregister = bpy.utils.register_classes_factory(classes)    


def register():
#   module_register()
    
    existing_shapekey_merger = operator_exists(ApplyModifierForObjectWithShapeKeysOperator.bl_idname)
    armature.module_register()
    shapekeys.module_register()


def unregister():
#   module_unregister()
    
    existing_shapekey_merger = operator_exists(ApplyModifierForObjectWithShapeKeysOperator.bl_idname)
  
    armature.module_unregister()
    shapekeys.module_unregister()
