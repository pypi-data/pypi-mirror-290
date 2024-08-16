#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File    ：show_image.py
# @Author  ：Jay
# @Date    ：2024/8/16 14:50 
# @Remark  ：
import cv2


# 显示图像
def show_image(image, window_name='Image'):
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 缩小图像
def resize_image(image, scale_factor):
    # 计算新的尺寸
    new_scale_factor = 1 / scale_factor
    new_size = (int(image.shape[1] * new_scale_factor), int(image.shape[0] * new_scale_factor))
    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)
    return resized_image


# 扣去空白透明背景
def strip_transparency(image):
    circle_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x, y, w, h = cv2.boundingRect(cv2.findNonZero(circle_gray))
    return image[y:y + h, x:x + w]


__all__ = ["show_image", "resize_image", "strip_transparency"]
