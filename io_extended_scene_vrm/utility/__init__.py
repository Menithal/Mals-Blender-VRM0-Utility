import re

blender_copy_re = re.compile("\.\d{3}$")
# https://blenderartists.org/t/how-to-know-if-an-operator-is-registered/638803/4
def operator_exists(idname):
    from bpy.ops import op_as_string
    try:
        op_as_string(idname)
        return True
    except:
        return False
 

def select_vrm_data(obj):

    if (obj is None):  raise Exception("No Object")
    extension = getattr(obj.data, "vrm_addon_extension", None)
    if extension is None: raise Exception("VRM Addon extension not detected on object")
    if extension.spec_version != "0.0": raise Exception ("Does not support any other version than 0.0 currently")

    return extension

def is_vrm0(obj):
    if (obj is None):
        return False

    extension = getattr(obj.data, "vrm_addon_extension", None)
    if(extension is None):
        return False
    
    return (extension.spec_version == "0.0")


# bpy.data.armatures["Armature"].vrm_addon_extension.spec_version