# coding=utf-8
from .utility import *
import numpy as np
from .color_histogram import doColorHistogram
from .color_layout import doColorLayout

def run(image, result, grid, data_set, mode, **kwargs):

    # ===== load image =====
    try:
        img = Image.open(image)
        pixel = img.load()
        width, height = img.size
        blockW, blockH = width/float(grid), height/float(grid)
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
        block = block.resize((int(blockW), int(blockH)))
        img.paste(block, (int(blockW*(i%grid)), int(blockH*int(i/grid))))

    img.save(result)


def histogram(img, pixel, width, height, blockW, blockH, grid, data_set, extension):

    # ===== cutting image =====
    imgData = [None]*pow(grid, 2)
    for i in range(grid * grid):
        w = (int)(i % grid)
        h = (int)(i / grid)
        # print w, h
        data = doColorHistogram(pixel, int(blockW), int(blockH), width*w/grid, height*h/grid)
        imgData[i] = np.array(data)


    # ===== finding tiles =====
    distances = [-1]*pow(grid, 2)
    tiles = [None]*pow(grid, 2)

    data_files = [f for f in os.listdir(data_set) if f.endswith(extension)]
    for i in range(len(data_files)):
        filename = data_files[i]

        with open(data_set + filename) as f:
            print("comparing file "+filename)
            compareData = [int(item) for item in f.read().splitlines()]
            f.close()

            for j in range(pow(grid, 2)):
                combine = list(map(lambda x: abs(x[0] - x[1]), zip(np.array(compareData), imgData[j])))
                for y in range(360):
                    if combine[y] > 180:
                        combine[y] = (360 - combine[y])
                    # combine[y] = combine[y] * 2
                for y in range(360, 562):
                    combine[y] = combine[y] / 2
                    # pass
                distance = np.linalg.norm(combine)

                if distance < distances[j] or distances[j] == -1:
                    distances[j] = distance
                    tiles[j] = filename.replace(extension, "")

    return tiles


def layout(img, pixel, width, height, blockW, blockH, grid, data_set, extension):

    # ===== cutting image =====
    imgData = [None]*pow(grid, 2)
    for i in range(grid * grid):
        w = (int)(i % grid)
        h = (int)(i / grid)
        # print w, h
        data = doColorHistogram(pixel, int(blockW), int(blockH), width*w/grid, height*h/grid)
        imgData[i] = np.array(data)

    dataY = [None]*pow(grid, 2)
    dataCb = [None]*pow(grid, 2)
    dataCr = [None]*pow(grid, 2)
    for i in range(grid * grid):
        w = (int)(i % grid)
        h = (int)(i / grid)
        # print w, h
        dataY[i], dataCb[i], dataCr[i] = doColorLayout(pixel, int(blockW), int(blockH), width*w/grid, height*h/grid)

    # ===== finding tiles =====
    distances = [-1]*pow(grid, 2)
    tiles = [None]*pow(grid, 2)

    data_files = [f for f in os.listdir(data_set) if f.endswith(extension)]
    for i in range(len(data_files)):
        filename = data_files[i]

        with open(data_set + filename) as f:
            print("comparing file "+filename)
            compareData = [item.split(' ') for item in f.read().splitlines()]
            f.close()
            compY = [float(j[0]) for j in compareData]
            compCb = [float(j[1]) for j in compareData]
            compCr = [float(j[2]) for j in compareData]

            for j in range(grid * grid):
                imgY, imgCb, imgCr = dataY[j], dataCb[j], dataCr[j]

                disY = [pow(imgY[k] - compY[k], 2) for k in range(64)]
                disCb = [pow(imgCb[k] - compCb[k], 2) for k in range(64)]
                disCr = [pow(imgCr[k] - compCr[k], 2) for k in range(64)]

                distance = pow(sum(disY), 0.5) + pow(sum(disCb), 0.5) + pow(sum(disCr), 0.5)

                if distance < distances[j] or distances[j] == -1:
                    distances[j] = distance
                    tiles[j] = filename.replace(extension, "")

    return tiles
