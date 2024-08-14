import bpy
from tqdm import tqdm

def create_transparent_material(obj, color, name):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.node_tree.nodes.clear()
    
    node_principled = mat.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    node_output = mat.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    
    mat.node_tree.links.new(node_principled.outputs['BSDF'], node_output.inputs['Surface'])
    
    node_principled.inputs['Base Color'].default_value = color
    node_principled.inputs['Alpha'].default_value = color[3]
    
    mat.blend_method = 'BLEND'
    
    obj.data.materials.append(mat)

def create_progress_bar(total):
    return tqdm(total=total, desc="進捗", bar_format="{l_bar}{bar}")
