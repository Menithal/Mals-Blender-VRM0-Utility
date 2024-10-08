import bpy
from io_extended_scene_vrm.shapekeys.references.vrm import vrm_shapekeys
# Groups to Set Presets for (VRM Presets)

def has_shapekey_in_mesh(shape_key: str, mesh: bpy.types.Object) -> bool:
    if mesh.type != "MESH": raise Exception("Expecting a Mesh")
    return shape_key.lower() in [item.name.lower() for item in mesh.data.shape_keys.key_blocks]


def bind_shapekeys_to_proxy(armature: bpy.types.Object, 
        shapekey: str, meshes: list[bpy.types.Object], group, retarget: dict = {}) -> None:
    
    armature_name = armature.name
    blendshape_groups = [item.lower() for item in armature.data.vrm_addon_extension.vrm0.blend_shape_master.blend_shape_groups.keys()]
    if shapekey in vrm_shapekeys:
        group.preset_name = shapekey.lower()
    
    mesh_names = []
    for bind in group.binds:
        if bind.mesh.mesh_object_name not in mesh_names:
            mesh_names.append(bind.mesh.mesh_object_name)
    
    retarget_keys = [item.lower() for item in retarget.keys()]

    ind = 0
    for mesh in meshes:         
        if mesh.type != "MESH": raise Exception("Expecting a Mesh")
        if mesh.name == "": continue #Empty name, ignore.
        if mesh.name in mesh_names: continue #mesh is already bound, ignore.

        is_retargetable = retarget is not None and shapekey.lower() in retarget_keys
        if is_retargetable:
            retarget_value = retarget.get(shapekey)
            if has_shapekey_in_mesh(retarget_value, mesh):
                # use original blendshapegroup
                blend_shape_group_index = blendshape_groups.index(shapekey.lower())
                bpy.ops.vrm.add_vrm0_blend_shape_bind(armature_name=armature_name, 
                                                    blend_shape_group_index=blend_shape_group_index)
                # use the retarget value instead.
                get_original_index = [item.name.lower() for item in mesh.data.shape_keys.key_blocks].index(retarget_value.lower())
                original_shapekey_name = mesh.data.shape_keys.key_blocks[get_original_index].name
                
                group.binds[ind].mesh.mesh_object_name = mesh.name
                group.binds[ind].index = original_shapekey_name
                ind+=1

        elif has_shapekey_in_mesh(shapekey, mesh):
            blend_shape_group_index = blendshape_groups.index(shapekey.lower())
            bpy.ops.vrm.add_vrm0_blend_shape_bind(armature_name=armature_name, 
                                                  blend_shape_group_index=blend_shape_group_index)
            
            get_original_index = [item.name.lower() for item in mesh.data.shape_keys.key_blocks].index(shapekey.lower())
            original_shapekey_name = mesh.data.shape_keys.key_blocks[get_original_index].name
            
            group.binds[ind].mesh.mesh_object_name = mesh.name
            group.binds[ind].index = original_shapekey_name
            ind+=1
        

def clear_vrm_blendshape_groups(armature: bpy.types.Object) -> None:
    if armature.type != "ARMATURE": raise Exception("Armature was not selected")
    if "vrm_addon_extension" not in armature.data: raise Exception("VRM Addon extension not detected on armature")
    
    blendshape_master = armature.data.vrm_addon_extension.vrm0.blend_shape_master

    # Deletes all EXISTING Groups
    for x in blendshape_master.blend_shape_groups:
        bpy.ops.vrm.remove_vrm0_blend_shape_group(armature_name=armature.name, blend_shape_group_index=0)        


def bind_shapekeys_to_vrm_blendshape_proxy(armature: bpy.types.Object, target_shapekey_list: list[str], bind_existing: bool = True, retargeted: dict = {}) -> None:
    if armature.type != "ARMATURE": raise Exception("Armature was not selected")
    if "vrm_addon_extension" not in armature.data: raise Exception("VRM Addon extension not detected on armature")
   
    available_shapekey_list: list[str] = []
    available_mesh_children: list[bpy.types.Mesh] = []
    # Iterate through all the child objects (that are visible) on the armature, and complete binding)
    for child in armature.children:
       if child.name not in bpy.context.view_layer.objects.keys(): continue
       if child.type != "MESH": continue
       
       if child.data.shape_keys is None: continue
   
       available_mesh_children.append(child)
    
       for shape_key in child.data.shape_keys.key_blocks:
          if shape_key in available_shapekey_list: continue    
          available_shapekey_list.append(shape_key.name.lower())

    existing_keys = [item.lower() for item in armature.data.vrm_addon_extension.vrm0.blend_shape_master.blend_shape_groups.keys()]
    skipped = 0
    
    for i,target_shapekey in enumerate(target_shapekey_list):  
        if (bind_existing and target_shapekey.lower() in available_shapekey_list) or not bind_existing:
            if target_shapekey.lower() not in existing_keys:
                print(target_shapekey)
                bpy.ops.vrm.add_vrm0_blend_shape_group(armature_name=armature.name, name=target_shapekey)

            group = armature.data.vrm_addon_extension.vrm0.blend_shape_master.blend_shape_groups[target_shapekey]
            bind_shapekeys_to_proxy(armature, target_shapekey, available_mesh_children, group, retargeted)
        else:
            skipped = skipped + 1
    
    if skipped > 0:
        print("Skipped creating ", skipped, " shapekeys that did not exist in any child mesh of vrm.")
    