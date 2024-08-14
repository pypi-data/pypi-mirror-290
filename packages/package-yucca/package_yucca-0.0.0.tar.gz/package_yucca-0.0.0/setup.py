from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='package_yucca',  
      version='0.0.0',
      description='A small example package',
      long_description=long_description,
      author='yuccatang',
      author_email='herrtangvonjj@gmail.com',
      install_requires=[],
      license='MIT License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )