import bpy

from io_extended_scene_vrm.shapekeys import shapekey_util
from io_extended_scene_vrm.shapekeys.references.vsf import vsf_shapekeys
from io_extended_scene_vrm.shapekeys.references.arkit import arkit_shapekeys
from io_extended_scene_vrm.shapekeys.references.meta import meta_shapekeys
from io_extended_scene_vrm.shapekeys.references.htc import htc_shapekeys
from io_extended_scene_vrm.shapekeys.references.vrm import vrm_shapekeys
from io_extended_scene_vrm.shapekeys.references.vrc import vsf_vrc_bindings
from io_extended_scene_vrm.shapekeys.references.mmd import mmd_shapekeys
from io_extended_scene_vrm.skeleton import skeleton_util

category = "VRM0 MalAv Tools"
class SHAPE_OT_VRM_EXTRA_Clear_All_Proxy_Shapekeys(bpy.types.Operator):
    """  Clear VRM of ALL Blendshape Proxy binds """
    bl_idname = "io_extended_scene_vrm.clear_all_shapekeys"
    bl_label = "Clear All Blendshape Proxy Binds"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        shapekey_util.clear_vrm_blendshape_groups(context.active_object)
        return {'FINISHED'}
    

class SHAPE_OT_VRM_EXTRA_Add_VRM_Shapekey(bpy.types.Operator):
    """ Generate and Bind all the Shapekeys found related to VRM """
    bl_idname = "io_extended_scene_vrm.bind_vrm_shape_keys"
    bl_label = "Generate and Bind VRM Shapekeys"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        shapekey_util.bind_shapekeys_to_vrm_blendshape_proxy(context.active_object, vrm_shapekeys, False)
        return {'FINISHED'}
    
class SHAPE_OT_VRM_EXTRA_Add_VSF_Shapekey(bpy.types.Operator):
    """Generate and Bind all the Shapekeys found related to VSF + VRM  """
    bl_idname = "io_extended_scene_vrm.bind_vsf_shape_keys"
    bl_label = "Generate and Bind VSF Shapekeys"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        shapekey_util.bind_shapekeys_to_vrm_blendshape_proxy(context.active_object, vsf_shapekeys, False)
        return {'FINISHED'}
    
    
class SHAPE_OT_VRM_EXTRA_Add_VRC_to_VSF_Shapekey(bpy.types.Operator):
    """Generate and Bind all the VCR Shapekeys found related to VSF + VRM  """
    bl_idname = "io_extended_scene_vrm.bind_vrc_vsf_shape_keys"
    bl_label = "Generate VSF Shapekeys out of VRC"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        shapekey_util.bind_shapekeys_to_vrm_blendshape_proxy(context.active_object, vsf_shapekeys, False, vsf_vrc_bindings)
        return {'FINISHED'}
    
    
class SHAPE_OT_VRM_EXTRA_Add_Arkit_Shapekeys(bpy.types.Operator):
    """ Generate and Bind all the Shapekeys found related to Arkit Facetracking  """
    bl_idname = "io_extended_scene_vrm.bind_arkit_shape_keys"
    bl_label = "Generate and Bind ARkit Shapekeys"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        shapekey_util.bind_shapekeys_to_vrm_blendshape_proxy(context.active_object, arkit_shapekeys, False)
        return {'FINISHED'}

class SHAPE_OT_VRM_EXTRA_Add_Meta_Shapekeys(bpy.types.Operator):
    """ Generate and Bind all the Shapekeys found related to Meta Facetracking  """
    bl_idname = "io_extended_scene_vrm.bind_meta_shape_keys"
    bl_label = "Generate and Bind Meta Shapekeys"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        shapekey_util.bind_shapekeys_to_vrm_blendshape_proxy(context.active_object, meta_shapekeys, False)
        return {'FINISHED'}
    
class SHAPE_OT_VRM_EXTRA_Add_HTC_Shapekeys(bpy.types.Operator):
    """ Generate and Bind ALL the Shapekeys found related to HTC Facetracking """
    bl_idname = "io_extended_scene_vrm.bind_htc_shape_keys"
    bl_label = "Generate and Bind HTC Shapekeys"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        shapekey_util.bind_shapekeys_to_vrm_blendshape_proxy(context.active_object, htc_shapekeys, False)
        return {'FINISHED'}

class SHAPE_OT_VRM_EXTRA_Add_MMD_Shapekeys(bpy.types.Operator):
    """ Bind the Shapekeys usually associated with MMD that exist in the child mesh """
    bl_idname = "io_extended_scene_vrm.bind_mmd_shape_keys"
    bl_label = "Bind Existing MMD Shapekeys"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        shapekey_util.bind_shapekeys_to_vrm_blendshape_proxy(context.active_object, mmd_shapekeys)
        return {'FINISHED'}

    
class SHAPE_PT_VRM_EXTENDED_BLENDSHAPE_PROXY_TOOLSET(bpy.types.Panel):
    """ Panel for Shapekey related tools """
    bl_label = "VRM 0.x Blendshape Proxy Extra Tools"
    bl_icon = "OBJECT_DATA"
    bl_space_type = "VIEW_3D"  
    bl_region_type = "UI"
    bl_category = category

    @classmethod
    def poll(self, context):
        contextIsObject = (context.mode == "OBJECT")
        selectedHasArmatureParent = skeleton_util.find_armature(context.selected_objects) is not None or (context.active_object is not None and context.active_object.type == "ARMATURE")
        activeIsVrm = context.active_object is not None and ("vrm_addon_extension" in context.active_object.data and 
                                                             "vrm0" in context.active_object.data.vrm_addon_extension)
        return  contextIsObject and selectedHasArmatureParent and activeIsVrm

    def draw(self, context):
        layout = self.layout
        layout.operator(SHAPE_OT_VRM_EXTRA_Add_VRM_Shapekey.bl_idname, icon="SHAPEKEY_DATA")
        layout.operator(SHAPE_OT_VRM_EXTRA_Add_VSF_Shapekey.bl_idname, icon="SHAPEKEY_DATA")
        layout.operator(SHAPE_OT_VRM_EXTRA_Add_VRC_to_VSF_Shapekey.bl_idname, icon="SHAPEKEY_DATA")
        layout.operator(SHAPE_OT_VRM_EXTRA_Add_Arkit_Shapekeys.bl_idname, icon="SHAPEKEY_DATA")
        layout.operator(SHAPE_OT_VRM_EXTRA_Add_Meta_Shapekeys.bl_idname, icon="SHAPEKEY_DATA")
        layout.operator(SHAPE_OT_VRM_EXTRA_Add_HTC_Shapekeys.bl_idname, icon="SHAPEKEY_DATA")
        layout.operator(SHAPE_OT_VRM_EXTRA_Add_MMD_Shapekeys.bl_idname, icon="SHAPEKEY_DATA")
        layout.operator(SHAPE_OT_VRM_EXTRA_Clear_All_Proxy_Shapekeys.bl_idname, icon="TRASH")
        
        return None 
    

classes = (
   SHAPE_PT_VRM_EXTENDED_BLENDSHAPE_PROXY_TOOLSET,
   SHAPE_OT_VRM_EXTRA_Add_VRM_Shapekey,
   SHAPE_OT_VRM_EXTRA_Clear_All_Proxy_Shapekeys,
   SHAPE_OT_VRM_EXTRA_Add_Arkit_Shapekeys,
   SHAPE_OT_VRM_EXTRA_Add_VSF_Shapekey,
   SHAPE_OT_VRM_EXTRA_Add_VRC_to_VSF_Shapekey,
   SHAPE_OT_VRM_EXTRA_Add_Meta_Shapekeys,
   SHAPE_OT_VRM_EXTRA_Add_HTC_Shapekeys,
   SHAPE_OT_VRM_EXTRA_Add_MMD_Shapekeys,

)

module_register, module_unregister = bpy.utils.register_classes_factory(classes)    


def register_module():
    module_register()


def unregister_module():
    module_unregister()