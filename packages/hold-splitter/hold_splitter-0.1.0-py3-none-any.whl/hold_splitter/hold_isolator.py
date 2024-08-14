# hold_splitter/hold_isolator.py

import bpy
import os
from loguru import logger

class HoldIsolator:
    def __init__(self):
        self.holds_collection = None

    def load_blend_file(self, file_path):
        logger.info(f"Blendファイルを読み込んでいます: {file_path}")
        bpy.ops.wm.open_mainfile(filepath=file_path)

    def save_blend_file(self, file_path):
        logger.info(f"結果を保存しています: {file_path}")
        bpy.ops.wm.save_as_mainfile(filepath=file_path)

    def separate_disconnected_meshes(self, obj):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.mode_set(mode='OBJECT')

    def create_collection(self, name):
        if name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(new_collection)
        return bpy.data.collections[name]

    def isolate_and_organize_holds(self, holds_obj_name="Holds"):
        logger.info("ホールドを分離し整理しています...")
        
        holds_obj = bpy.data.objects.get(holds_obj_name)
        if not holds_obj:
            logger.error(f"'{holds_obj_name}'オブジェクトが見つかりません。")
            return

        # 繋がっていないメッシュを分離
        self.separate_disconnected_meshes(holds_obj)

        # 新しいコレクションを作成
        self.holds_collection = self.create_collection("Isolated_Holds")

        # 分離されたオブジェクトを新しいコレクションに移動
        for obj in bpy.context.selected_objects:
            if obj.name.startswith(holds_obj_name):
                # オブジェクトが属しているすべてのコレクションからアンリンク
                for coll in obj.users_collection:
                    coll.objects.unlink(obj)
                # 新しいコレクションにリンク
                self.holds_collection.objects.link(obj)
                
        logger.info(f"{len(self.holds_collection.objects)}個のホールドを分離し、整理しました。")

    def get_isolated_holds_count(self):
        return len(self.holds_collection.objects) if self.holds_collection else 0

    def run(self, input_file, output_file, holds_obj_name="Holds"):
        self.load_blend_file(input_file)
        self.isolate_and_organize_holds(holds_obj_name)
        self.save_blend_file(output_file)
        logger.info(f"分離されたホールドの数: {self.get_isolated_holds_count()}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="HoldIsolator: ホールドを分離し整理する")
    parser.add_argument("input_file", help="入力Blendファイルのパス")
    parser.add_argument("output_file", help="出力Blendファイルのパス")
    parser.add_argument("--holds_obj_name", default="Holds", help="ホールドオブジェクトの名前")
    args = parser.parse_args()

    isolator = HoldIsolator()
    isolator.run(args.input_file, args.output_file, args.holds_obj_name)
