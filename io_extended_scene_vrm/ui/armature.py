import bpy

import re 
from io_extended_scene_vrm.skeleton import skeleton_util
from io_extended_scene_vrm.utility import blender_copy_re

category = "VRM0 MalAv Tools"
class ARMATURE_OT_VRM_EXTRA_Create_Armature(bpy.types.Operator):
    """ Create Reference VRM Armature directly in scene in T pose """
    bl_idname = "io_extended_scene_vrm.create_reference"
    bl_label = "Create Reference VRM Armature"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"
    # TODO: Make sure T-Pose is at 100 scale instead of tiny
    def execute(self, context):
        skeleton_util.build_skeleton()
        return {'FINISHED'}
    

class ARMATURE_OT_VRM_EXTRA_Set_Pose_Operator(bpy.types.Operator):
    """ Tool to quickly set the skeleton pose into a reference VRM T Pose, 
    This allows you to TEST rolls, rotations, and adjust bone positions before final binding """
    bl_idname = "io_extended_scene_vrm.set_t_pose"
    bl_label = "Test T-Pose"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    @classmethod
    def poll(self, context):
        enabled = False
        for selected_object in context.selected_objects:
            enabled = enabled or selected_object.data.get("vrm_addon_extension") 
        return context.mode == "OBJECT"

    def execute(self, context):
        armature = skeleton_util.find_armature(context.selected_objects)
        armature.location.x = 0
        armature.location.z = 0
        armature.location.y = 0
        # TODO: If Adjusting Hips, Adjust hips position to make sure that bounding box of the entire armature has the feet touching the plane
        skeleton_util.pose_to_vrm_reference(context,context.selected_objects)
        return {'FINISHED'}
    

# TODO: Check that T Pose is  applied, If ANY BONES are moved, Cancel and Dialog Warn.
class ARMATURE_OT_VRM_EXTRA_Bind_T_Pose_Operator(bpy.types.Operator):
    """ This should be your FINAL step before Export. Any customization should be baked down before attempting to use this.
     Does the Following Actions
    - Duplicates VRM armature and all its child objects to do Operations on
    - Puts The new Duplicates to "Final-VRM-Export" Collection and adds -VRM to end of the Mesh and Armature
    - Forces T pose, 
    - Applies new T Pose armature for ALL Shapekeys, This may take a while (note: HIGHLY DESTRUCTIVE: May cause some issues with using tool mirrorings)
    - Sets the T Pose as final rest pose (note: HIGHLY DESTRUCTIVE: existing animations need to be retargeted for new rest pose)
    """
    bl_idname = "io_extended_scene_vrm.bind_t_pose_asset"
    bl_label = "Finalize T-Pose"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    @classmethod
    def poll(self, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        # TODO: Duplicate and Apply all 
        print("Starting io_extended_scene_vrm.bind_t_pose_asset")
        armature = skeleton_util.find_armature(context.selected_objects)

        print("Found Armature, Cloning Armature and Existing visible children")
               
        for obj in context.selected_objects:
            obj.select_set(False)
        
        for child in armature.children:
            if child.hide_get() == True: continue
            print("Selecting",child.name)
            child.select_set(True)
        armature.select_set(True)

        print("Duplicating")
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
        
        # Hide Originals
        print("Hide Originals for their safety")
        armature.hide_set(True)
        for child in armature.children:
            child.hide_set(True)
        
        if "VRM-Export" not in bpy.data.collections:
            print("Creating missing collection")
            bpy.data.collections.new("VRM-Export") # Create Collection
            bpy.data.collections["VRM-Export"].color_tag = "COLOR_07"
            bpy.context.scene.collection.children.link(bpy.data.collections["VRM-Export"]) # Link new Collection to Scene

        print("Moving Duplicates to VRM-Export Collection")
        for obj in context.selected_objects:
            obj.name = re.sub( blender_copy_re, "-VRM", obj.name)
            for collection in obj.users_collection:
                collection.objects.unlink(obj)
            bpy.data.collections["VRM-Export"].objects.link(obj) # Add to T-Pose-Bound collection
        
        newArmature = skeleton_util.find_armature(context.selected_objects)

        newArmature.location.x = 0
        newArmature.location.z = 0
        newArmature.location.y = 0
        #TODO: Move this out
        print("Zeroing 3DCursor")
        bpy.context.scene.cursor.location[0] = 0.0
        bpy.context.scene.cursor.location[1] = 0.0
        bpy.context.scene.cursor.location[2] = 0.0

        print("Selecting The new duplicates")
        
        for child in newArmature.children:
            child.select_set(True)
        newArmature.select_set(True)

        print("Centering all duplicates to region zero, and applying transforms")
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    
        print("Posing to VRM Reference.")
        skeleton_util.pose_to_vrm_reference(context, [newArmature])
        
        bpy.ops.object.mode_set(mode="OBJECT")

        skeleton_util.apply_armature_restpose(context, newArmature)

        return {'FINISHED'}

    
class ARMATURE_OT_VRM_EXTRA_Bind_As_SpringBone_Group(bpy.types.Operator):
    """
        Auto Binds Basic Colliders, like Hands, and Fingers. Skips If they exist
        Binds these colliders to existing Springbone proxies. 
    """
    bl_idname = "io_extended_scene_vrm.bind_springbone_colliders"
    bl_label = "Autobind SpringBone Collider Groups"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):
        return {'FINISHED'}
    
class ARMATURE_OT_VRM_EXTRA_Bind_As_SpringBone_Group(bpy.types.Operator):
    """
        Creates a new Springbone group from selected bones. Adds existing Springbone Colliders to The group
    """
    bl_idname = "io_extended_scene_vrm.set_selected_as_springbones"
    bl_label = "Add Selected as Springbone Group"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):

        secondary_animation = context.active_object.data.vrm_addon_extension.vrm0.secondary_animation
        next_index = len(secondary_animation.bone_groups)

        bpy.ops.vrm.add_vrm0_secondary_animation_group(armature_name=context.active_object.name)
        selected_bone_group = secondary_animation.bone_groups[next_index]
        selected_bone_group.comment = "Generated Springbone Group " + str(next_index+1)

        # Same Default as UniVRM
        selected_bone_group.gravity_dir[2] = -1
        selected_bone_group.hit_radius = 0.03
        selected_bone_group.stiffiness = 1
        selected_bone_group.drag_force = 0.4

        bones = context.selected_pose_bones or context.selected_bones
        for bone_index, bone in enumerate(bones):
            bpy.ops.vrm.add_vrm0_secondary_animation_group_bone(armature_name=context.active_object.name, bone_group_index=next_index)
            selected_bone_group.bones[bone_index].bone_name = bone.name
            
        return {'FINISHED'}


class ARMATURE_OT_VRM_EXTRA_Bind_As_SpringBoneCollider_Group(bpy.types.Operator):
    """
        Creates a new Springbone Collider from selected bones. 
    """
    bl_idname = "io_extended_scene_vrm.set_selected_as_springbone_colliders"
    bl_label = "Add Selected as Springbone Group Colliders"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"

    def execute(self, context):

        secondary_animation = context.active_object.data.vrm_addon_extension.vrm0.secondary_animation
        current_length = len(secondary_animation.collider_groups)
        
        bones = context.selected_pose_bones or context.selected_bones
        for bone_index, bone in enumerate(bones):
            bpy.ops.vrm.add_vrm0_secondary_animation_collider_group(armature_name=context.active_object.name)
            secondary_animation.collider_groups[current_length].node.bone_name = bone.name
            bpy.ops.vrm.add_vrm0_secondary_animation_collider_group_collider(armature_name=context.active_object.name, 
                                                                             collider_group_index=current_length, bone_name=bone.name)
            current_length = current_length + 1
        
        return {'FINISHED'}

    
class ARMATURE_OT_VRM_EXTRA_Clear_SpringBoneColliders(bpy.types.Operator):
    """
    Clears VRM Springbone colliders from the selected VRM Skeleton
    """
    bl_idname = "io_extended_scene_vrm.clear_springbone_colliders"
    bl_label = "Clear Springbone Collider Groups"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"
    def execute(self, context):
        secondary_animation = context.active_object.data.vrm_addon_extension.vrm0.secondary_animation
        for bone in secondary_animation.collider_groups:
            for collider in bone.colliders:
                bpy.ops.vrm.remove_vrm0_secondary_animation_collider_group_collider(armature_name=context.active_object.name, collider_group_index=0, collider_index=0)
            
            bpy.ops.vrm.remove_vrm0_secondary_animation_collider_group(armature_name=context.active_object.name, collider_group_index=0)

        return {'FINISHED'}


class ARMATURE_OT_VRM_EXTRA_Clear_SpringBones(bpy.types.Operator):
    """
    Clears VRM Springbone  from the selected VRM Skeleton
    """
    bl_idname = "io_extended_scene_vrm.clear_springbones"
    bl_label = "Clear Springbone Groups"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = category
    bl_space_type = "VIEW_3D"
    
    def execute(self, context):
        secondary_animation = context.active_object.data.vrm_addon_extension.vrm0.secondary_animation
        for bone in secondary_animation.bone_groups:
           bpy.ops.vrm.remove_vrm0_secondary_animation_group(armature_name=context.active_object.name, bone_group_index=0)

        return {'FINISHED'}



class ARMATURE_PT_VRM_ARMATURE_EXTENDED_TOOLSET(bpy.types.Panel):
    """ Panel for VRMArmature related tools """
    bl_label = "VRM 0.x Armature Extra Tools"
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
        return contextIsObject and selectedHasArmatureParent and activeIsVrm

    def draw(self, context):
        layout = self.layout

        layout.operator(ARMATURE_OT_VRM_EXTRA_Create_Armature.bl_idname,  icon='ARMATURE_DATA')
        layout.operator(ARMATURE_OT_VRM_EXTRA_Set_Pose_Operator.bl_idname,  icon='OUTLINER_OB_ARMATURE')
        layout.operator(ARMATURE_OT_VRM_EXTRA_Bind_T_Pose_Operator.bl_idname,  icon='OUTLINER_OB_ARMATURE')

        return None 
    

class ARMATURE_PT_VRM_ARMATURE_SPRINGBONES_EXTENDED_TOOLSET(bpy.types.Panel):
    """ Panel for VRM Springbone related tools """
    bl_label = "VRM 0.x Springbone Extra Tools"
    bl_icon = "OBJECT_DATA"
    bl_space_type = "VIEW_3D" 
    bl_region_type = "TOOLS"

    @classmethod
    def poll(self, context):
        contextIsObject = (context.mode == "POSE" or context.mode == "EDIT_ARMATURE")
        selectedHasArmatureParent = skeleton_util.find_armature(context.selected_objects) is not None or (context.active_object is not None and context.active_object.type == "ARMATURE")
        activeIsVrm = context.active_object is not None and ("vrm_addon_extension" in context.active_object.data and 
                                                             "vrm0" in context.active_object.data.vrm_addon_extension)
        return contextIsObject and selectedHasArmatureParent and activeIsVrm

    def draw(self, context):
        layout = self.layout
        layout.operator(ARMATURE_OT_VRM_EXTRA_Bind_As_SpringBone_Group.bl_idname, icon='OUTLINER_DATA_ARMATURE')
        layout.operator(ARMATURE_OT_VRM_EXTRA_Bind_As_SpringBoneCollider_Group.bl_idname, icon='OUTLINER_DATA_ARMATURE')
        layout.operator(ARMATURE_OT_VRM_EXTRA_Clear_SpringBones.bl_idname, icon='TRASH')
        layout.operator(ARMATURE_OT_VRM_EXTRA_Clear_SpringBoneColliders.bl_idname, icon='TRASH')
        
        return None 


classes = (
    ARMATURE_OT_VRM_EXTRA_Create_Armature,
    ARMATURE_OT_VRM_EXTRA_Set_Pose_Operator,
    ARMATURE_OT_VRM_EXTRA_Bind_T_Pose_Operator,
    ARMATURE_PT_VRM_ARMATURE_EXTENDED_TOOLSET,
    ARMATURE_OT_VRM_EXTRA_Bind_As_SpringBone_Group,
    ARMATURE_OT_VRM_EXTRA_Clear_SpringBones,
    ARMATURE_OT_VRM_EXTRA_Bind_As_SpringBoneCollider_Group,
    ARMATURE_OT_VRM_EXTRA_Clear_SpringBoneColliders,
    ARMATURE_PT_VRM_ARMATURE_SPRINGBONES_EXTENDED_TOOLSET
) 

module_register, module_unregister = bpy.utils.register_classes_factory(classes)    


def register_module():
    module_register()

def unregister_module():
    module_unregister()
