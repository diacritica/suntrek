#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import collections
import datetime
import json

import settings

#today = datetime.date.today() fixme with zfill
urlwithfile = "http://www.swpc.noaa.gov/ftpdir/lists/xray/Gp_xr_5m.txt"

"""
:Data_list: Gs_xr_5m.txt
:Created: 2012 Oct 23 1605 UTC
# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center
# Please send comments and suggestions to SWPC.Webmaster@noaa.gov 
# 
# Label: Short = 0.05- 0.4 nanometer
# Label: Long  = 0.1 - 0.8 nanometer
# Units: Short = Watts per meter squared
# Units: Long  = Watts per meter squared
# Source: GOES-15
# Location: W135
# Missing data: -1.00e+05
#
#                         GOES-15 Solar X-ray Flux
# 
#                 Modified Seconds
# UTC Date  Time   Julian  of the
# YR MO DA  HHMM    Day     Day       Short       Long        Ratio
#-------------------------------------------------------------------
2012 10 23  1405   56223  50700     4.84e-08    1.55e-06    3.13e-02
2012 10 23  1410   56223  51000     4.68e-08    1.52e-06    3.09e-02
2012 10 23  1415   56223  51300     4.54e-08    1.50e-06    3.04e-02
2012 10 23  1420   56223  51600     4.37e-08    1.46e-06    2.99e-02
2012 10 23  1425   56223  51900     4.34e-08    1.46e-06    2.97e-02
"""


def run():

    if settings.TEST == True:
        pass

    else:

        r = requests.get(urlwithfile)
        with open("output/Gp_xr_5m.txt","w") as fdurl:
            fdurl.write(r.text)
            fdurl.close()

        particle_map = {}
        fdfile = open("output/Gp_xr_5m.txt","r")
        fdshortf = open("output/solarxrayshortflux.txt","w")
        fdlongf = open("output/solarxraylongflux.txt","w")
        
        particledatetimelist = []
        xrayshortdatalist = []
        xraylongdatalist = []

        for line in fdfile:
            values = line.strip().split()
            if len(values) == 9:
                YR,MO,DA,HHMM,GDay,GSec,S,L,R = values
                particledatetime = datetime.datetime(int(YR),int(MO), \
                                                         int(DA),int(HHMM[:2]), \
                                                         int(HHMM[2:])).isoformat()

                particledatetimelist.append(particledatetime)

                xrayshortdatalist.append(float(S))
                xraylongdatalist.append(float(L))


        xrayshortdict = {"label":"Short (0.05 - 0.4 nm) W/m2)","legendEntry":True, "fitType": "spline",
                   "data" : {
                "x" : particledatetimelist,
                "y" : xrayshortdatalist,                
                },
                   "markers" : {
                "visible" : False, "type" : "circle",
                },

                   }
        jsontext = json.dumps(xrayshortdict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fdshortf.write(jsontext)
        fdshortf.close()


        xraylongdict = {"label":"Long (0.1 - 0.8 nm) W/m2)","legendEntry":True, "fitType": "spline",
                   "data" : {
                "x" : particledatetimelist,
                "y" : xraylongdatalist,                
                },
                   "markers" : {
                "visible" : False, "type" : "circle",
                },

                   }
        jsontext = json.dumps(xraylongdict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fdlongf.write(jsontext)
        fdlongf.close()



if __name__ == '__main__':
    run()

