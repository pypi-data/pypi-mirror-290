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
    version='1.0.2',
    author='Jay',
    description='Verification code image recognition!',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jaygarage/bouncing',
    packages=find_packages(),
    install_requires=[
        'opencv-python>=4.10.0.84',
        'xxhash>=3.4.1',
        'cachetools>5.3.3',
        'numpy>=1.25.2',
        'scikit-image>=0.19.3',
        'requests>=2.32.3',
        'fake_useragent>=1.5.1',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7'
)
