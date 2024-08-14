from distutils.core import  setup
import setuptools
packages = ['cduprem']# 唯一的包名，自己取名
setup(name='cduprem',
	version='1.0.8',
	author='cth',
    packages=packages, 
    package_dir={'requests': 'requests'},
    include_package_data=True,)
    
