# coding=utf-8
from setuptools import setup

setup(name='mosaic_image',
      version='0.1',
      description='An API to process a mosaic image with serveral images',
      #url='',
      author='Colman',
      author_email='colman0423@gmail.com',
      package=['mosaic_image'],
      entry_points={
            'console_scripts': [
                'create-mosaic-data=mosaic_image.create_mosaic_data:run'
            ]
      }
      )