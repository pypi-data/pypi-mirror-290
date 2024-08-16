#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @File    ：setup.py
# @Author  ：Jay
# @Date    ：2024/6/21 18:41 
# @Remark  ：
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='bouncing',
    version='1.0.1',
    author='Jay',
    description='Verification code image recognition!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jaygarage/bouncing',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'xxhash',
        'cachetools',
        'numpy',
        'scikit-image',
        'curl_cffi',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
