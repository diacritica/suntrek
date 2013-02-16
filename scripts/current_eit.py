#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests


from StringIO import StringIO

import settings

basepath = "http://sohowww.nascom.nasa.gov/data/LATEST/"
giffiles = ["current_c2.gif", "current_eit_304.gif", "current_eit_195.gif", "current_eit_171.gif", "current_eit_284.gif"]

def run():

    if settings.TEST == True:
        pass

    else:

        for giffilename in giffiles:
            r = requests.get(basepath + giffilename)
            print(giffilename + str(r.status_code))
            i = open("output/gifs/" + giffilename, "w")
            i.write(r.content)
            i.close()
            print(giffilename + " saved")

if __name__ == "__main__":
    run()
