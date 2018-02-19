# coding=utf-8
from .utility import *
from .color_histogram import doColorHistogram
from .color_layout import doColorLayout


def createData(data_path, mode):
    extension = "."+mode
    listdir = os.listdir(data_path)
    imageList = [f for f in listdir if isImage(f)]
    dtList = [f for f in listdir if f.endswith(extension)]
    for image_name in imageList:
        try:
            dtList.index(image_name + extension)
        except ValueError:
            print(image_name)
            img = Image.open(data_path + image_name)
            pixel = img.load()
            width, height = img.size

            if mode == COLOR_HISTOGRAM:
                hsvArr = doColorHistogram(pixel, width, height)
                file = open(data_path + image_name + extension, "w")
                for i in hsvArr:
                    print(str(i), file=file)
                file.close()

            elif mode == COLOR_LAYOUT:
                dataY, dataCb, dataCr = doColorLayout(pixel, width, height)
                file = open(data_path + image_name + extension, "w")
                for i in range(64):
                    print(str(dataY[i]) + ' ' + str(dataCb[i]) + ' ' + str(dataCr[i]), file=file)
                file.close()

            else:
                raise Exception("mode not found")


def create(data_path, mode):
    print("start creating...")
    flag = False

    if mode.find(COLOR_HISTOGRAM)!=-1:
        createData(data_path, COLOR_HISTOGRAM)
        flag = True
    if mode.find(COLOR_LAYOUT) != -1:
        createData(data_path, COLOR_LAYOUT)
        flag = True
    if not flag:
        raise Exception("mode not found")

    print("create data end")


def run():
    import sys
    arg1, arg2 = DEFAULT_DATA_PATH, COLOR_HISTOGRAM + COLOR_LAYOUT
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
    except:
        pass
    print(arg1, arg2)
    create(arg1, arg2)

