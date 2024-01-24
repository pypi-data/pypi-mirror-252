#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 2024

@author: nmngo
@version: 0.1
"""

from setuptools import setup

setup(name='likewines',
      description='Comparison and predictive analysis of wines',
      author='Ngoc Minh Ngo',
      version='0.1',
      packages=['likewines.model', 'likewines.processor'],
      package_dir={'likewines.model': './model',
                   'likewines.processor': './processor'},
      install_requires=['tensorflow==2.15.0', 'pandas==2.1.4',
                        'pyarrow==11.0.0', 'numpy==1.24.3',
                        'scikit-learn==1.3.0', 'joblib==1.2.0']
      )
