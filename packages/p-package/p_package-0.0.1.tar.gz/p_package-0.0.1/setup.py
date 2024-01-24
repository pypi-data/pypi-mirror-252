# setup.py
from setuptools import setup, find_packages

setup(
   name="p_package",
   author="unknow",
   description="unknow",
   packages=find_packages(),
   include_package_data=True,
   classifiers=[
    "Development Status :: 3 - Alpha",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
],
   python_requires='>=3.6',
   setup_requires=['setuptools-git-versioning'],
   version_config={
       "dirty_template": "{tag}",
   }
)