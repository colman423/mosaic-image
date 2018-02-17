# coding=utf-8
from .utility import *

def run(image_path, data_path, mode, create_data_first, **kwargs):
    if create_data_first:
        from .create_mosaic_data import create
        create(data_path, mode)



    pass