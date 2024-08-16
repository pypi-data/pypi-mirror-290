#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File    ：__init__.py.py
# @Author  ：Jay
# @Date    ：2024/8/16 15:00 
# @Remark  ：
import cv2
from bouncing.utils import ttl_cache, load_image, strip_transparency


# 读取缺口图
@ttl_cache(ttl=120, maxsize=1000)
def load_slider_image(notch_image_item, threshold1, threshold2):
    """
    @param notch_image_item: 图片数据；可以是文件路径、url、数组
    @param threshold1: first threshold for the hysteresis procedure.
    @param threshold2: second threshold for the hysteresis procedure.
    @return: 返回原图、调优之后的图
    """
    notch_image = load_image(notch_image_item)
    notch_image_go_blank = strip_transparency(notch_image)

    notch_image_go_blank = cv2.GaussianBlur(notch_image_go_blank, (1, 1), 1)  # 高斯滤波器模糊图像
    notch_image_go_blank_gray = cv2.cvtColor(notch_image_go_blank, cv2.COLOR_BGR2GRAY)  # 灰度化
    notch_image_edges = cv2.Canny(notch_image_go_blank_gray, threshold1=threshold1, threshold2=threshold2)  # 边缘匹配

    return notch_image, cv2.cvtColor(notch_image_edges, cv2.COLOR_GRAY2RGB)  # 灰度化


def discern(
        slider_image, notch_image,
        slider_image_threshold1=100, slider_image_threshold2=200,
        notch_image_threshold1=100, notch_image_threshold2=200
):
    """
    识别滑块缺口
    @param slider_image: 滑块背景图
    @param notch_image: 缺口图
    @param slider_image_threshold1: first threshold for the hysteresis procedure.
    @param slider_image_threshold2: second threshold for the hysteresis procedure.
    @param notch_image_threshold1: first threshold for the hysteresis procedure.
    @param notch_image_threshold2: second threshold for the hysteresis procedure.
    @return: 缺口四角坐标
    """
    original_slider_image, slider_image = load_slider_image(slider_image, slider_image_threshold1, slider_image_threshold2)
    original_notch_image, notch_image = load_slider_image(notch_image, notch_image_threshold1, notch_image_threshold2)

    slider_image = slider_image[:300, ::]
    result = cv2.matchTemplate(slider_image, notch_image, cv2.TM_CCOEFF_NORMED)  # 寻找最优匹配
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)  # 最优结果

    br = tuple(map(lambda x, y: x + y, max_loc, notch_image.shape[:2]))  #  右下角点的坐标

    cv2.rectangle(original_slider_image, max_loc, br, (0, 255, 0), 1)  # 绘制矩形
    return (max_loc, br), original_slider_image  # 匹配结果，一般使用max_loc[0]
