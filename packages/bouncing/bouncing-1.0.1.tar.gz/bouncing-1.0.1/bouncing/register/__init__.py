#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File    ：__init__.py
# @Author  ：Jay
# @Date    ：2024/8/12 13:57
# @Remark  ：
import cv2
import numpy as np
from skimage.draw import circle_perimeter
from concurrent.futures import ThreadPoolExecutor
from bouncing.utils import ttl_cache, resize_image, load_image, show_image


# 计算两个总的颜色在 HSV (色调、饱和度、明度) 色彩空间中的距离
def calculate_color_deviation(inner_circle_points, outer_circle_points):
    # 截取图片形状相同长度
    min_len = min(len(inner_circle_points), len(outer_circle_points))
    inner_circle_points = inner_circle_points[:min_len]
    outer_circle_points = outer_circle_points[:min_len]

    # 使用 NumPy 向量化操作计算色调差异（考虑了环绕效应）
    hue_diff = np.minimum(
        np.abs(inner_circle_points[:, 0] - outer_circle_points[:, 0]),
        360 - np.abs(inner_circle_points[:, 0] - outer_circle_points[:, 0])
    )

    # 计算饱和度和明度的差异
    saturation_diff = np.abs(inner_circle_points[:, 1] - outer_circle_points[:, 1])
    value_diff = np.abs(inner_circle_points[:, 2] - outer_circle_points[:, 2])

    # 计算总的颜色偏差
    distance = np.sqrt(hue_diff ** 2 + saturation_diff ** 2 + value_diff ** 2)
    return np.sum(distance)


# 获取圆周上的点
def get_circle_points(img, radius):
    rows, cols, _ = img.shape
    center = (cols // 2, rows // 2)

    # 生成圆周上的点坐标
    rr, cc = circle_perimeter(center[1], center[0], radius, method='andres')

    # 确保坐标在图像范围内
    valid_indices = (0 <= rr) & (rr < rows) & (0 <= cc) & (cc < cols)
    rr = rr[valid_indices]
    cc = cc[valid_indices]

    # 提取圆周上的点的颜色值
    circle_points = img[rr, cc]
    return np.array(circle_points)


# 计算最佳角度
@ttl_cache(ttl=120, maxsize=1000)
def calculate_deviation(inner_image, rotation_center, angle, pic_circle_radius, outer_circle_points, pic_circle_radius_size):
    # 旋转内图像
    matrix = cv2.getRotationMatrix2D(rotation_center, angle, 1)
    inner_rotated = cv2.warpAffine(inner_image, matrix, (inner_image.shape[1], inner_image.shape[0]), flags=cv2.INTER_NEAREST)

    # 获取旋转后的内图像圆周上的点
    inner_circle_points = get_circle_points(inner_rotated, pic_circle_radius - pic_circle_radius_size)

    # 计算总的颜色偏差
    return angle, calculate_color_deviation(inner_circle_points, outer_circle_points)


# 读取图片
@ttl_cache(ttl=120, maxsize=1000)
def read_image(image: bytes, resize: int):
    original_image = load_image(image, cv2.IMREAD_COLOR)
    new_image = resize_image(original_image, resize)  # 缩小图片提速
    return cv2.cvtColor(new_image, cv2.COLOR_BGR2HSV), original_image  # 转换到 HSV 颜色空间，输出原图


def identify(
        outer_image_brg_bytes,
        inner_image_brg_bytes,
        display: bool = False,
        start_angle: int = 150,
        angle_jump: int = 5,
        pic_circle_radius: int = 24,
        resize: int = 4,
        pic_circle_radius_size: int = 1
):
    """
    在外部图像中寻找最适合的角度，以使内部图像与外部图像的颜色匹配最接近

    :param outer_image_brg_bytes: 外部图像的路径（BGR格式）。
    :param inner_image_brg_bytes: 内部图像的路径（BGR格式）。
    :param display: 是否显示旋转完成的图片，默认不显示。
    :param start_angle: 起始角度，默认150。
    :param angle_jump: 循环检测角度跳跃， 默认3。
    :param pic_circle_radius: 圆周点的半径，用于提取图像的圆周点。
    :param resize: 图像缩放因子。缩小图像时，实际缩放因子为 1 / resize。
    :param pic_circle_radius_size: 圆周点半径调整值，用于获取外图像的圆周点。
    :return: 最佳的旋转角度，以使得内部图像与外部图像的颜色匹配最接近。
    """
    with ThreadPoolExecutor() as executor:
        # 加载内外图像
        [inner_image, original_inner_image], [outer_image, original_outer_image] = list(executor.map(
            lambda ib: read_image(image=ib, resize=resize),
            [inner_image_brg_bytes, outer_image_brg_bytes]
        ))

        # 获取外图像圆周上的点
        outer_circle_points = get_circle_points(outer_image, pic_circle_radius + pic_circle_radius_size)
        # 预计算旋转中心
        rotation_center = (inner_image.shape[1] // 2, inner_image.shape[0] // 2)

        # 遍历旋转角度以寻找最佳匹配
        results = list(
            executor.map(
                lambda angle: calculate_deviation(inner_image, rotation_center, angle, pic_circle_radius, outer_circle_points, pic_circle_radius_size),
                range(start_angle, 361, angle_jump)
            )
        )

        # 找到最小偏差的角度
        best_angle, min_deviation = min(results, key=lambda x: x[1])

    if display:
        # 旋转内图像
        inner_rotated_image = cv2.warpAffine(
            original_inner_image,
            cv2.getRotationMatrix2D((original_inner_image.shape[1] // 2, original_inner_image.shape[0] // 2), best_angle, 1),
            (original_inner_image.shape[1], original_inner_image.shape[0])
        )

        # 创建一个全零的蒙版，大小与外图像相同
        mask = np.zeros_like(original_outer_image)

        # 计算内图像放置的起始坐标，以便中心对齐
        start_x = (original_outer_image.shape[1] - inner_rotated_image.shape[1]) // 2
        start_y = (original_outer_image.shape[0] - inner_rotated_image.shape[0]) // 2

        # 将旋转后的内图像放置到蒙版的中心位置
        mask[start_y:start_y + inner_rotated_image.shape[0], start_x:start_x + inner_rotated_image.shape[1]] = inner_rotated_image

        # 合成图像：将内图像的有效区域叠加到外图像上
        combined_image = cv2.addWeighted(original_outer_image, 1, mask, 1, 1)
        show_image(combined_image, "Result Graph")

    return best_angle


__all__ = ["identify"]
