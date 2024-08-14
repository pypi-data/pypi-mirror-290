# hold_splitter/wall_hold_splitter.py

import bpy
from mathutils import Vector
from .blender_utils import ensure_unique_object_name

def clean_mesh(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.fill_holes()
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode='OBJECT')

def reset_scale_and_origin(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

def apply_boolean_with_high_precision(obj, cut_obj, operation):
    bool_mod = obj.modifiers.new(name="Boolean", type='BOOLEAN')
    bool_mod.object = cut_obj
    bool_mod.operation = operation
    bool_mod.solver = 'EXACT'
    bool_mod.use_self = True
    # bool_mod.threshold = 0.000001

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier="Boolean")

def cleanup_after_boolean(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.mesh.delete_loose()
    bpy.ops.object.mode_set(mode='OBJECT')

def split_wall_and_holds_boolean(imported_obj, wall_plane):
    # メッシュのクリーンアップと最適化
    clean_mesh(imported_obj)
    reset_scale_and_origin(imported_obj)

    # 元のオブジェクトを複製
    wall_obj = imported_obj.copy()
    wall_obj.data = imported_obj.data.copy()
    wall_obj.name = ensure_unique_object_name("Wall")
    bpy.context.collection.objects.link(wall_obj)

    holds_obj = imported_obj.copy()
    holds_obj.data = imported_obj.data.copy()
    holds_obj.name = ensure_unique_object_name("Holds")
    bpy.context.collection.objects.link(holds_obj)

    # 高精度のBoolean操作を適用
    apply_boolean_with_high_precision(wall_obj, wall_plane, 'DIFFERENCE')
    apply_boolean_with_high_precision(holds_obj, wall_plane, 'INTERSECT')

    # Boolean操作後のクリーンアップ
    cleanup_after_boolean(wall_obj)
    cleanup_after_boolean(holds_obj)

    # 元のオブジェクトを削除
    bpy.data.objects.remove(imported_obj, do_unlink=True)

    return wall_obj, holds_obj

def adjust_wall_plane(wall_plane, imported_obj):
    bbox_center = sum((Vector(b) for b in imported_obj.bound_box), Vector()) / 8
    wall_plane.location = imported_obj.matrix_world @ bbox_center

def offset_wall_plane(wall_plane, offset):
    if len(wall_plane.data.polygons) > 0:
        normal = wall_plane.data.polygons[0].normal
        wall_plane.location += normal * offset
