#!/bin/env python
# setup.py
from setuptools import setup, find_packages

#
setup(name='hy_alipay_sdk',

      version='0.1',


      description='hy_alipay_sdk enterprise edition',

      packages=find_packages(),


      zip_safe=False

 )

# setup(
#     setup_requires=['pbr', 'setuptools'],
#     pbr=True,
#     test_suite='tests._test',
# )