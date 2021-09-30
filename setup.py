from setuptools import setup, find_packages

setup(name='minermanager',
      packages=find_packages(),
      package_data={'': ['*.yaml', '*.yml']})