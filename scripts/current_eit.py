#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

from PIL import Image
from StringIO import StringIO

import settings

basepath = "http://sohowww.nascom.nasa.gov/data/LATEST/"
giffiles = ["current_c2small.gif", "current_eit_304small.gif", "current_eit_195small.gif", "current_eit_171small.gif", "current_eit_284small.gif"]

def run():

    if settings.TEST == True:
        pass

    else:

        for giffilename in giffiles:
            r = requests.get(basepath + giffilename)
            print(giffilename + str(r.status_code))
            i = Image.open(StringIO(r.content))
            i.save("output/gifs/" + giffilename)
            print(giffilename + " saved")

if __name__ == "__main__":
    run()
