
import bpy
from mathutils import Matrix, Vector
from .vrm_skeleton import skeleton as vrm_skeleton, index_bindings


def find_armature(selection):
    for selected in selection:
        if selected.type == "ARMATURE":
            return selected
        if selected.type == "MESH" and selected.parent is not None and selected.parent.type == "ARMATURE":
            return selected.parent
    return None

def pose_armature(armature,current_bindings, data, current_rest_node, world_matrix, parent, parent_node):
    name = current_rest_node["name"]

    # refere to the bindings dictionary, get index to use in indexbindings when match with reference skeleton
    reference_name = None
    if index_bindings.get(name) is not None:  
        reference_name = current_bindings[index_bindings[name]]

    if reference_name is None: 
        return
    
    bone = data.get(reference_name)
    if(bone):
        armature.data.bones[bone.name].select = True
        legacy_rotation = bone.rotation_mode
        bone.rotation_mode = "QUATERNION"
        # bpy.ops.action.keyframe_insert()
        destination_matrix = current_rest_node["matrix_local"].copy()
        inv_destination_matrix = destination_matrix.inverted()
        matrix = bone.matrix
        if parent:
            parent_matrix = parent.matrix.copy()
            parent_inverted = parent_matrix.inverted()
            parent_destination = parent_node["matrix_local"].copy()
        else:
            parent_matrix = Matrix()
            parent_inverted = Matrix()
            parent_destination = Matrix()
            
        smat = inv_destination_matrix @ \
            (parent_destination @ (parent_inverted @ matrix))
        quat_inv = smat.to_quaternion().inverted()
        bone.rotation_quaternion = quat_inv
        
        bone.rotation_mode = legacy_rotation
        
        # If Keyframes are being followed,make sure to keep track of them
        # 
        if(bpy.context.scene.tool_settings.use_keyframe_insert_auto):
            bpy.ops.anim.keyframe_insert_by_name(type="Rotation")

        armature.data.bones[bone.name].select = False
        for child in current_rest_node["children"]:
            pose_armature(armature,current_bindings, data, child, world_matrix,
                              bone, current_rest_node)
    else:
        bone = parent
        for child in current_rest_node["children"]:
            pose_armature(armature,data, child, world_matrix, bone, parent_node)

def get_current_vrm_bindings(selected):
    vrm_binding = dict()

    if(selected.data.get("vrm_addon_extension") is None):
        raise Exception("Not a VRM Model or not been processed by VRM Blender Addon")

    human_bones = selected.data.vrm_addon_extension.vrm0.humanoid.human_bones
    for i,bone in enumerate(human_bones):
        vrm_binding[i] = bone.node.bone_name
    
    return vrm_binding

def pose_to_vrm_reference(selected: list[bpy.types.Object]) -> None:
    armature = find_armature(selected)
    if armature is not None:
        current_vrm_bindings = get_current_vrm_bindings(armature)
        # Center Children First
        bpy.context.view_layer.objects.active = armature
        armature.select_set(state=True)
        bpy.context.object.data.pose_position = 'POSE'

        bpy.ops.object.mode_set(mode="OBJECT")
        # Make sure to reset the bones first.
        bpy.ops.object.transform_apply(
            location=False, rotation=True, scale=True)

        bpy.ops.object.mode_set(mode="POSE")
        bpy.ops.pose.select_all(action="SELECT")
        bpy.ops.pose.transforms_clear()
        bpy.ops.pose.select_all(action="DESELECT")

        world_matrix = armature.matrix_world
        bones = armature.pose.bones

        for bone in vrm_skeleton:
            pose_armature(armature,current_vrm_bindings, bones, bone, world_matrix, None, None)

        print("Moving Next")

        armature.select_set(state=True)
        bpy.ops.object.mode_set(mode="OBJECT")

        print("Done")
    else:
        print("No Armature, select, throw an exception")
        raise Exception("You must have an armature to continue")



def build_armature_structure(data, current_node, parent):

    name = current_node["name"]
    bpy.ops.armature.bone_primitive_add(name=name)

    current_bone_index = data.edit_bones.find(name)
    current_bone = data.edit_bones[current_bone_index]

    current_bone.parent = parent

    current_bone.head = current_node["head"]
    current_bone.tail = current_node["tail"]
    mat = current_node["matrix"]
    current_bone.matrix = mat

    if current_node["connect"]:
        current_bone.use_connect = True

    for child in current_node["children"]:
        build_armature_structure(data, child, current_bone)

    return current_bone


def build_skeleton():
    current_view = bpy.context.area.type
    try:
        bpy.context.area.type = "VIEW_3D"
        # set context to 3D View and set Cursor
        bpy.context.scene.cursor.location[0] = 0.0
        bpy.context.scene.cursor.location[1] = 0.0
        bpy.context.scene.cursor.location[2] = 0.0

        if bpy.context.active_object:
            bpy.ops.object.mode_set(mode="OBJECT")

        bpy.ops.object.add(type="ARMATURE", enter_editmode=True)

        current_armature = bpy.context.active_object

        current_armature.name = "Armature"
        for root_bone in vrm_skeleton:
            build_armature_structure(current_armature.data, root_bone, None)

        current_armature.scale = Vector((100.0, 100.0, 100.0))
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        

        
    except Exception as detail:
        print("Error", detail)

    finally:
        bpy.context.area.type = current_view
