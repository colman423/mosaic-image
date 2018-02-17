# coding=utf-8
from .utility import COLOR_HISTOGRAM, COLOR_LAYOUT

def mosaic(image_path=".", data_path="./dataset/", mode=COLOR_HISTOGRAM, create_data_first=True, **kwargs):
    from .calculate_mosaic import run
    run(image_path=image_path, data_path=data_path, mode=mode, create_data_first=create_data_first, **kwargs)

