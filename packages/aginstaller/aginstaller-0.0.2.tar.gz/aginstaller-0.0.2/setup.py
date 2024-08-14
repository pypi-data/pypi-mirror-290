from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='aginstaller',    # 包名
      version='0.0.1',        # 版本号
      description='aginstall beta',
      long_description=long_description,
      author='ldp',
      author_email='bruceamadeuslee@gmail.com',
      url='',
      install_requires=["loguru"],	# 依赖包会同时被安装
      license='MIT',
      packages=find_packages())
