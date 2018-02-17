# coding=utf-8
from .utility import *
import numpy as np
from .color_histogram import doColorHistogram

def run(image, result, grid, data_set, mode, **kwargs):

    # ===== load image =====
    try:
        img = Image.open(image)
        pixel = img.load()
        width, height = img.size
        blockW, blockH = int(round(width / float(grid))), int((height / float(grid)))
    except:
        raise Exception("invalid input image")

    # ===== mode dependency =====
    tiles = []
    if mode==COLOR_HISTOGRAM:
        tiles = histogram(img, pixel, width, height, blockW, blockH, grid, data_set, "."+mode)
    elif mode==COLOR_LAYOUT:
        tiles = layout(img, pixel, width, height, blockW, blockH, grid, data_set, "."+mode)
    else:
        raise Exception("mode not found")


    # ===== assembling new image =====
    for i in range(pow(grid, 2)):
        tile = tiles[i]
        # print "tiles[{0}] = {1}".format(i, tile)
        block = Image.open(data_set + tile)
        block = block.resize((blockW, blockH))
        img.paste(block, (blockW * (i % grid), blockH * int(i / grid)))

    img.save(result)


def histogram(img, pixel, width, height, blockW, blockH, grid, data_set, extension):

    # ===== cutting image =====
    imgData = [None]*pow(grid, 2)
    for i in range(grid * grid):
        w = (int)(i % grid)
        h = (int)(i / grid)
        # print w, h
        data = doColorHistogram(pixel, blockW, blockH, width * w / grid, height * h / grid)
        imgData[i] = np.array(data)


    # ===== finding tiles =====
    colorDis = [-1]*pow(grid, 2)
    tiles = [None]*pow(grid, 2)

    filedata = [f for f in os.listdir(data_set) if f.endswith(extension)]
    datacount = len(filedata)
    for i in range(datacount):
        filename = filedata[i]

        with open(data_set + filename) as f:
            print("comparing file "+filename)
            compareData = [int(item) for item in f.read().splitlines()]
            f.close()

            for j in range(pow(grid, 2)):
                combine = list(map(lambda x: abs(x[0] - x[1]), zip(np.array(compareData), imgData[j])))
                for y in range(360):
                    if combine[y] > 180:
                        combine[y] = (360 - combine[y])
                    combine[y] =combine[y] * 2
                for y in range(360, 461):
                    combine[y] = combine[y] / 2
                distance = np.linalg.norm(combine)

                if distance < colorDis[j] or colorDis[j] == -1:
                    colorDis[j] = distance
                    tiles[j] = filename.replace(extension, "")

    return tiles


def layout(img, pixel, width, height, blockW, blockH, grid, data_set, extension):


    # ===== cutting image =====
    imgData = [None]*pow(grid, 2)
    for i in range(grid * grid):
        w = (int)(i % grid)
        h = (int)(i / grid)
        # print w, h
        data = doColorHistogram(pixel, blockW, blockH, width * w / grid, height * h / grid)
        imgData[i] = np.array(data)


    # ===== finding tiles =====

    colorDis = [-1]*pow(grid, 2)
    tiles = [None]*pow(grid, 2)

    filedata = [f for f in os.listdir(data_set) if f.endswith(extension)]
    datacount = len(filedata)
    for i in range(datacount):
        filename = filedata[i]

        with open(data_set + filename) as f:
            print("comparing file "+filename)
            compareData = [int(item) for item in f.read().splitlines()]
            f.close()

            for j in range(pow(grid, 2)):

                combine = list(map(lambda x: abs(x[0] - x[1]), zip(np.array(compareData), imgData[j])))
                for y in range(360):
                    if combine[y] > 180:
                        combine[y] = (360 - combine[y])
                    combine[y] =combine[y] * 2
                for y in range(360, 461):
                    combine[y] = combine[y] / 2
                distance = np.linalg.norm(combine)

                if distance < colorDis[j] or colorDis[j] == -1:
                    colorDis[j] = distance
                    tiles[j] = filename.replace(extension, "")

    return tiles