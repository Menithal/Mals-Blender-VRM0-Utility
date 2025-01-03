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
from .ui import armature, shapekeys

bl_info = { 
    "name": "Mals' Extended VRM",
    "author": "Matti 'Menithal' Lahtinen", 
    "version": (0, 0, 12),
    "blender": (3, 3, 0),
    "location": "3D View Tools",
    "description": "Additional VRM Tools",
    "warning": "",
    "wiki_url": "", 
    "support": "COMMUNITY",
    "category": "Addon Extension",
}

def register():
    armature.module_register()
    shapekeys.module_register()


def unregister():
    armature.module_unregister()
    shapekeys.module_unregister()
