# coding=utf-8
import colorsys


def doColorHistogram(pixel, width, height, xStart=0, yStart=0):
    hArr = [0 for i in range(360)]
    sArr = [0 for i in range(101)]
    vArr = [0 for i in range(101)]
    # print "info:", width, height, xStart, yStart
    pixArr = [pixel[x+xStart, y+yStart] for x in range(width) for y in range(height)]
    hsvArr = [colorsys.rgb_to_hsv(item[0]/255., item[1]/255., item[2]/255.) for item in pixArr]

    for item in hsvArr:
        hAdjust = int(round(item[0]*360))
        if hAdjust == 360:
            hAdjust = 0
        hArr[hAdjust] += 1
        sArr[int(round(item[1]*100))] += 1
        vArr[int(round(item[2]*100))] += 1

    return hArr+sArr+vArr