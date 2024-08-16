#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File    ：load_image.py
# @Author  ：Jay
# @Date    ：2024/8/16 14:42 
# @Remark  ：
import os
import re
import cv2
import numpy
import base64
from curl_cffi import requests
from fake_useragent import UserAgent

userAgent = UserAgent()


# 读取图片
def load_image(image_item, flags=cv2.IMREAD_UNCHANGED) -> numpy.ndarray:
    """

    支持：图片array数组、图片list数组，图片路径，图片url
    @param image_item: numpy数组、多维图片数组列表、图片路径、图片链接
    @param flags: 读取图片的模式
    @return:
    """
    image_type = type(image_item)

    if image_type == numpy.ndarray:
        return image_item

    elif image_type == list:
        return numpy.asarray(image_item, dtype=numpy.uint8)

    elif image_type == str and os.path.exists(image_item):
        return cv2.imread(image_item, flags=flags)

    elif image_type == bytes:
        return cv2.imdecode(
            numpy.frombuffer(image_item, numpy.uint8),
            flags=flags  # 读取图片模式
        )

    elif image_type == str and bool(re.findall(fr'{image_item[0]}.t\w{{0,2}}://', image_item)):
        return cv2.imdecode(
            numpy.frombuffer(
                requests.get(url=image_item, headers={'User-Agent': userAgent.random}).content,  # 下载图片
                numpy.uint8  # 类型转换
            ),
            flags=flags  # 读取图片模式
        )
    else:
        try:
            return cv2.imdecode(
                numpy.frombuffer(
                    base64.b64decode(image_item), numpy.uint8
                ),
                flags=flags
            )
        except Exception as _:
            raise Exception("输入的数据类型不正确...")


#  保存在本地
def save_image(image, path="new_img.png"):
    cv2.imwrite(path, image)


__all__ = ["load_image", "save_image"]
