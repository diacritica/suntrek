#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import datetime

from PIL import Image
from StringIO import StringIO

import settings


today = datetime.date.today()
yesterday = today - datetime.timedelta(1)

basepath = "http://www.spaceweather.com/images%s/%s/"%(today.strftime("%Y"),today.strftime("%d%b%y").lower())
fallbackbasepath = "http://www.spaceweather.com/images%s/%s/"%(today.strftime("%Y"),yesterday.strftime("%d%b%y").lower())

imagefiles = ["hmi240.gif", "hmi4096_blank.jpg"]
textfiles = ["sunspot_labels.txt"]

size = 600,600

def run():

    if settings.TEST == True:
        pass

    else:

        for imgfilename in imagefiles:
            try:
                r = requests.get(basepath + imgfilename)
                print(imgfilename + str(r.status_code))
                i = Image.open(StringIO(r.content))
                i.thumbnail(size, Image.ANTIALIAS)
                i.save("output/gifs/" + imgfilename)
                print(imgfilename + " saved")
            except:
                r = requests.get(fallbackbasepath + imgfilename)
                print(imgfilename + str(r.status_code))
                i = Image.open(StringIO(r.content))
                i.thumbnail(size, Image.ANTIALIAS)
                i.save("output/gifs/" + imgfilename)
                print(imgfilename + " saved")
                basepath = fallbackbasepath

        for txtfilename in textfiles:
            r = requests.get(basepath + txtfilename)
            print(txtfilename + str(r.status_code))
            i = open("output/" + txtfilename, "w")
            i.write(r.content)
            i.close()
            print(txtfilename + " saved")


if __name__ == "__main__":
    run()
