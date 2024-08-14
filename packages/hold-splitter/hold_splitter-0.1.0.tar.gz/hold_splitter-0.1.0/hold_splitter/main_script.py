# hold_splitter/main_script.py

import subprocess
import sys
import os
import argparse
from loguru import logger

# Blenderの実行ファイルへのパス
BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe"

def run_blender_script(fbx_path, offset, split_threshold):
    # Blender内で実行するスクリプトのパス
    blender_script_path = os.path.join(os.path.dirname(__file__), "blender_script.py")
    logger.info(f"blender_script_path : {blender_script_path}")
    
    # Blenderをバックグラウンドモードで実行
    command = [
        BLENDER_PATH,
        "--background",
        "--python", blender_script_path,
        "--",
        fbx_path,
        str(offset),
        str(split_threshold)
    ]
    
    subprocess.run(command)

    # 新しい出力ファイル名を生成
    output_dir = os.path.dirname(fbx_path)
    output_path = os.path.join(output_dir, "isolated_holds_model.blend")
    
    logger.info(f"処理が完了しました。出力ファイル: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="HoldSplitter: クライミングウォールの平面を可視化")
    parser.add_argument("fbx_path", help="FBXファイルへのパス")
    parser.add_argument("--offset", type=float, default=0, help="壁面平面のオフセット値")
    parser.add_argument("--split_threshold", type=float, default=0.01, help="壁とホールドを分離する際のしきい値")
    args = parser.parse_args()

    run_blender_script(args.fbx_path, args.offset, args.split_threshold)

if __name__ == "__main__":
    main()
