# hold_splitter/blender_script.py

import bpy
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from hold_splitter.core import process_model
from hold_splitter.visualization import create_progress_bar
from hold_splitter.hold_isolator import HoldIsolator
from loguru import logger

def main():
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = []
    
    if len(argv) < 1:
        logger.error("エラー: FBXファイルのパスが指定されていません。")
        return

    fbx_path = argv[0]
    offset = float(argv[1]) if len(argv) > 1 else 0
    split_threshold = float(argv[2]) if len(argv) > 2 else 0.01

    logger.info(f"処理を開始します: {fbx_path}")
    logger.info(f"オフセット値: {offset}")
    logger.info(f"分割しきい値: {split_threshold}")

    progress_bar = create_progress_bar(6)  # 6ステップの進捗バー

    wall_obj, holds_obj, wall_plane = process_model(fbx_path, offset)

    if wall_obj is None or holds_obj is None or wall_plane is None:
        logger.error("処理に失敗しました。")
        return
    progress_bar.update(5)
    # 中間ファイルを保存
    intermediate_file = os.path.join(os.path.dirname(fbx_path), "intermediate_model.blend")
    bpy.ops.wm.save_as_mainfile(filepath=intermediate_file)

    # ホールドの分離と整理
    hold_isolator = HoldIsolator()
    hold_isolator.run(r"assets\a\source\finalized\intermediate_model.blend", r"assets\a\source\finalized\separated_model3.blend", holds_obj.name)
    progress_bar.update(6)

    # 結果の保存
    output_dir = os.path.dirname(fbx_path)
    output_path = os.path.join(output_dir, "isolated_holds_model.blend")
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    logger.info(f"結果を保存しました: {output_path}")
    logger.info(f"分離されたホールドの数: {hold_isolator.get_isolated_holds_count()}")

    logger.info("処理が完了しました。")

if __name__ == "__main__":
    main()
