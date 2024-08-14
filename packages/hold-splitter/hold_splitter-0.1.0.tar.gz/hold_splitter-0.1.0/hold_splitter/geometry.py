# hold_splitter/geometry.py

import numpy as np
from mathutils import Vector, Matrix
from .blender_utils import ensure_unique_object_name
import bpy

def find_dominant_normal(bm, angle_threshold=np.radians(10)):
    """
    主要な法線を見つけ、それに対応する面を特定します。

    :param bm: BMeshオブジェクト
    :param angle_threshold: 主要な法線との許容角度（ラジアン）
    :return: (主要な法線, 主要な面のセット)
    """
    normal_groups = {}
    for face in bm.faces:
        normal = tuple(round(n, 2) for n in face.normal)
        if normal not in normal_groups:
            normal_groups[normal] = []
        normal_groups[normal].append(face)
    
    dominant_normal = max(normal_groups, key=lambda n: len(normal_groups[n]))
    dominant_faces = set(normal_groups[dominant_normal])
    
    # 角度閾値内の面も含める
    for normal, faces in normal_groups.items():
        if normal != dominant_normal:
            dot_product = np.dot(dominant_normal, normal)
            dot_product = max(-1, min(1, dot_product))  # ドット積を-1から1の範囲に制限
            angle = np.arccos(dot_product)
            if angle < angle_threshold:
                dominant_faces.update(faces)
    
    return Vector(dominant_normal), dominant_faces

def create_wall_aligned_plane(vertices, normal, offset=0.005):
    """
    頂点群と法線に基づいて壁に沿った平面を作成します。

    :param vertices: 頂点のリスト
    :param normal: 法線ベクトル
    :param offset: 平面のオフセット値
    :return: 作成された平面オブジェクト
    """
    # 頂点をZ軸周りに90度回転
    rotation_matrix = Matrix.Rotation(np.radians(-90), 4, 'Z')
    rotated_vertices = [rotation_matrix @ Vector(v) for v in vertices]
    rotated_normal = rotation_matrix @ normal
    
    # 頂点をオフセット
    if offset != 0:
        offset_vector = Vector(rotated_normal) * offset
        rotated_vertices = [v + offset_vector for v in rotated_vertices]
    
    # 点群の中心を計算
    center = sum((Vector(v) for v in rotated_vertices), Vector()) / len(rotated_vertices)

    # 主成分分析（PCA）を使用して平面の向きを計算
    points = np.array(rotated_vertices) - center
    cov_matrix = np.cov(points.T)
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
    
    # 最小の固有値に対応する固有ベクトルが法線方向
    pca_normal = eigenvectors[:, np.argmin(eigenvalues)]
    
    # 元の法線との向きを合わせる
    if np.dot(pca_normal, rotated_normal) < 0:
        pca_normal = -pca_normal

    # 平面の回転を計算
    rotation = Vector(pca_normal).to_track_quat('-Z', 'Y')
    
    # 平面のサイズを計算
    projected_points = points @ eigenvectors
    min_coords = np.min(projected_points, axis=0)
    max_coords = np.max(projected_points, axis=0)
    size = max_coords - min_coords
    size = [max(s, 5) for s in size[:2]]  # 最小サイズを5に設定

    # 平面メッシュを作成
    bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, location=center)
    plane_obj = bpy.context.active_object
    plane_obj.name = ensure_unique_object_name("Wall_Aligned_Plane")
    plane_obj.rotation_euler = rotation.to_euler()
    plane_obj.scale = Vector((size[0], size[1], 1))
    
    return plane_obj

def offset_vertices(vertices, normal, offset):
    """
    頂点を法線方向に指定した距離だけオフセットします。

    :param vertices: 頂点のリスト
    :param normal: 法線ベクトル
    :param offset: オフセット距離
    :return: オフセットされた頂点のリスト
    """
    offset_vector = Vector(normal) * offset
    return [Vector(v) + offset_vector for v in vertices]

