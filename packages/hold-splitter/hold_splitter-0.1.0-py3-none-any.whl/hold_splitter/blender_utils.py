# hold_splitter/blender_utils.py

import bpy
from loguru import logger

def import_fbx(file_path):
    logger.info(f"FBXファイルをインポートしています: {file_path}")
    bpy.ops.import_scene.fbx(filepath=file_path)
    mesh_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    
    if not mesh_objects:
        logger.error("インポートされたFBXファイルにメッシュオブジェクトが含まれていません。")
        raise ValueError("インポートされたFBXファイルにメッシュオブジェクトが含まれていません。")
    
    logger.info(f"インポートされたメッシュオブジェクト数: {len(mesh_objects)}")
    logger.info(f"最初のメッシュオブジェクト名: {mesh_objects[0].name}")
    
    return mesh_objects[0]

def clear_scene():
    logger.info("シーンをクリアしています...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    logger.info("シーンのクリアが完了しました。")

def setup_scene():
    logger.info("シーンのセットアップを開始します...")
    
    # ワールドの背景色を設定
    bpy.context.scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.05, 0.05, 0.05, 1)
    logger.info("ワールドの背景色を設定しました。")

    # レンダリング設定
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.device = 'GPU'
    logger.info("レンダリングエンジンをCycles（GPU）に設定しました。")

    # カメラの設定
    bpy.ops.object.camera_add(location=(0, -10, 2), rotation=(1.5708, 0, 0))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera
    logger.info("カメラを追加し、シーンカメラとして設定しました。")

    # ライトの設定
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.active_object
    sun.data.energy = 2
    logger.info("サンライトを追加しました。")

    logger.info("シーンのセットアップが完了しました。")

def ensure_unique_object_name(name):
    logger.info(f"オブジェクト名 '{name}' のユニーク性を確保します。")
    if name in bpy.data.objects:
        base_name = name
        counter = 1
        while name in bpy.data.objects:
            name = f"{base_name}_{counter}"
            counter += 1
        logger.info(f"既存のオブジェクトが存在するため、名前を '{name}' に変更します。")
    return name
