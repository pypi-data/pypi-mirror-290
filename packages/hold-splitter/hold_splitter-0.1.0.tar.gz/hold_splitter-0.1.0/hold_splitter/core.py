# hold_splitter/core.py

import bpy
import bmesh
from .blender_utils import import_fbx, clear_scene, setup_scene, ensure_unique_object_name
from .geometry import find_dominant_normal, create_wall_aligned_plane
from .visualization import create_transparent_material, create_progress_bar
from .wall_hold_splitter import split_wall_and_holds_boolean, offset_wall_plane
from loguru import logger

def process_model(fbx_path, offset=0):
    logger.info("処理を開始します...")
    progress_bar = create_progress_bar(7)  # 7ステップの進捗バー

    logger.info("シーンをクリアしています...")
    clear_scene()
    progress_bar.update(1)

    logger.info("シーンをセットアップしています...")
    setup_scene()
    progress_bar.update(2)

    logger.info(f"FBXファイルをインポートしています: {fbx_path}")
    try:
        imported_obj = import_fbx(fbx_path)
        imported_obj.name = ensure_unique_object_name("Imported_Object")
    except ValueError as e:
        logger.error(f"FBXファイルのインポートに失敗しました: {str(e)}")
        return None, None, None
    progress_bar.update(3)

    logger.info("主要な法線を検出しています...")
    bm = bmesh.new()
    bm.from_mesh(imported_obj.data)
    dominant_normal, wall_component = find_dominant_normal(bm)
    vertices = [v.co for f in wall_component for v in f.verts]
    progress_bar.update(4)

    logger.info("壁面の平面を作成しています...")
    wall_plane = create_wall_aligned_plane(vertices, dominant_normal)
    progress_bar.update(5)

    logger.info(f"壁面をオフセットしています: {offset}")
    # offset_wall_plane(wall_plane, offset)
    progress_bar.update(6)

    logger.info("壁面の材質を設定しています...")
    create_transparent_material(wall_plane, color=(0, 1, 0, 0.3), name="Wall_Plane_Material")

    logger.info("壁とホールドを分離しています...")
    wall_obj, holds_obj = split_wall_and_holds_boolean(imported_obj, wall_plane)
    # wall_obj, holds_obj = True, True
    progress_bar.update(7)

    logger.info("処理が完了しました。")
    return wall_obj, holds_obj, wall_plane
