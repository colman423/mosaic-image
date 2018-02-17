# coding=utf-8
from .utility import COLOR_HISTOGRAM, COLOR_LAYOUT


def mosaic(image, result, grid=10, open=True, data_set="./dataset/", mode=COLOR_HISTOGRAM, create_data_first=True, **kwargs):
    if create_data_first:
        create_data(data_set, mode)

    from .calculate_mosaic import run
    run(image, result, grid, data_set, mode, **kwargs)

    if open:
        from subprocess import call
        call(result, shell=True)

def create_data(data_set="./dataset/", mode=COLOR_HISTOGRAM):
    from .create_mosaic_data import create
    create(data_path=data_set, mode=mode)