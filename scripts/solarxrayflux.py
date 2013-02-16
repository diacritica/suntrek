#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import collections
import datetime
import json

import settings

#today = datetime.date.today()
urlwithfile = "http://www.swpc.noaa.gov/ftpdir/lists/xray/Gp_xr_5m.txt"

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

