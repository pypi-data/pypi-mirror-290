# hold_splitter/cli.py

import argparse
import sys
import os
from .main_script import run_blender_script

def main():
    parser = argparse.ArgumentParser(description="HoldSplitter: クライミングウォールの平面を可視化")
    parser.add_argument("fbx_path", help="FBXファイルへのパス")
    parser.add_argument("--offset", type=float, default=0, help="壁面平面のオフセット値")
    args = parser.parse_args()

    run_blender_script(args.fbx_path, args.offset)

if __name__ == "__main__":
    main()
