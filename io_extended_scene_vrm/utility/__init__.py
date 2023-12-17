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
 