# coding=utf-8
import os
from PIL import Image

COLOR_HISTOGRAM = "histogram"
COLOR_LAYOUT = "layout"


DEFAULT_DATA_PATH = os.getcwd() + "/dataset/"


def isImage(f):
    return f.endswith('.jpg') or f.endswith('.png') or f.endswith('.bmp') or f.endswith('.gif')
