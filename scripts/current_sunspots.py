#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import datetime

from PIL import Image
from StringIO import StringIO

import settings


today = datetime.date.today()
basepath = "http://www.spaceweather.com/images%s/%s/"%(today.strftime("%Y"),today.strftime("%d%b%y").lower())

imagefiles = ["hmi240.gif", "hmi4096_blank.jpg"]
textfiles = ["sunspot_labels.txt"]

def run():

    if settings.TEST == True:
        pass

    else:

        for txtfilename in textfiles:
            r = requests.get(basepath + txtfilename)
            print(txtfilename + str(r.status_code))
            i = open("output/" + txtfilename, "w")
            i.write(r.content)
            print(txtfilename + " saved")

        for imgfilename in imagefiles:
            r = requests.get(basepath + imgfilename)
            print(imgfilename + str(r.status_code))
            i = Image.open(StringIO(r.content))
            i.save("output/gifs/" + imgfilename)
            print(imgfilename + " saved")


if __name__ == "__main__":
    run()
