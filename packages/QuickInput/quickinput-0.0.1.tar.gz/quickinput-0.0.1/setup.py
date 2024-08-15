from setuptools import setup, find_packages
setup(
name='QuickInput',
version='0.0.1',
author='tjf1',
author_email='tjf1dev@gmail.com',
description='A short description of your package',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
install_requires=[
    'colorama',
    'keyboard'
],
python_requires='>=3.6',
)