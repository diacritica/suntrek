#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json

from StringIO import StringIO

import settings

basepath = "http://sohowww.nascom.nasa.gov/data/LATEST/"

#For local connection, high quality
#giffiles = ["current_c2.gif", "current_eit_171.gif", "current_eit_195.gif", "current_eit_284.gif", "current_eit_304.gif"]

#For Internet connection, low quality
giffiles = ["current_c2small.gif", "current_eit_171small.gif", "current_eit_195small.gif", "current_eit_284small.gif", "current_eit_304small.gif"]

giffiles = [

giffilesdescription = ["Inner solar corona up to 8.4 million kilometers away from the star.",
                       "171 Angstrom - materials at 1 Million K",
                       "195 Angstrom - materials at 1.5 Million K",
                       "284 Angstrom - materials at 2 Million K",
                       "304 Angstrom - materials at 60.000 - 80.000 K",
                       ]

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

        fdfddf = open("output/current_eit.json","w")
        jsontext = json.dumps(giffilesdescription, sort_keys = True,
                              indent=4, separators=(',',': '))
        fdfddf.write(jsontext)
        fdfddf.close()
        

if __name__ == "__main__":
    run()
