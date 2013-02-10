#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import collections
import datetime
import json

import settings

urlwithfile = "http://www.swpc.noaa.gov/ftpdir/lists/particle/Gp_part_5m.txt"

def run():

    if settings.TEST == True:
        pass

    else:

        r = requests.get(urlwithfile)
        with open("output/Gp_part_5m.txt","w") as fdurl:
            fdurl.write(r.text)
            fdurl.close()

        particle_map = {}
        fdfile = open("output/Gp_part_5m.txt","r")
        fdp10f = open("output/solarparticleP10flux.txt","w")
        fdp100f = open("output/solarparticleP100flux.txt","w")
        fde08f = open("output/solarelectron08flux.txt","w")
        fde20f = open("output/solarelectron20flux.txt","w")
        
        particledatetimelist = []
        protonP10datalist = []
        protonP100datalist = []
        electronE08datalist = []
        electronE20datalist = []

        for line in fdfile:
            values = line.strip().split()
            if len(values) == 15:
                YR,MO,DA,HHMM,GDay,GSec,P1,P5,P10,P30,P50,P100,E08,E20,E40 = values
                particledatetime = datetime.datetime(int(YR),int(MO), \
                                                         int(DA),int(HHMM[:2]), \
                                                         int(HHMM[2:])).isoformat()

                particledatetimelist.append(particledatetime)

                protonP10datalist.append(float(P10))
                protonP100datalist.append(float(P100))
                electronE08datalist.append(float(E08))
                electronE20datalist.append(float(E20))



        P10dict = {"label":"P>10MeV","legendEntry":True, "fitType": "spline",
                   "data" : {
                "x" : particledatetimelist,
                "y" : protonP10datalist,                
                },
                   "markers" : {
                "visible" : False, "type" : "circle",
                },

                   }
        jsontext = json.dumps(P10dict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fdp10f.write(jsontext)
        fdp10f.close()

        P100dict = {"label":"P>100MeV","legendEntry":True, "fitType": "spline",
                   "data" : {
                "x" : particledatetimelist,
                "y" : protonP100datalist,                
                },
                   "markers" : {
                "visible" : False, "type" : "circle",
                },

                   }
        jsontext = json.dumps(P100dict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fdp100f.write(jsontext)
        fdp100f.close()


        E08dict = {"label":"E>0.8MeV","legendEntry":True, "fitType": "spline",
                   "data" : {
                "x" : particledatetimelist,
                "y" : electronE08datalist,                
                },
                   "markers" : {
                "visible" : False, "type" : "circle",
                },

                   }
        jsontext = json.dumps(E08dict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fde08f.write(jsontext)
        fde08f.close()

        E20dict = {"label":"E>2.0MeV","legendEntry":True, "fitType": "spline",
                   "data" : {
                "x" : particledatetimelist,
                "y" : electronE20datalist,                
                },
                   "markers" : {
                "visible" : False, "type" : "circle",
                },

                   }
        jsontext = json.dumps(E20dict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fde20f.write(jsontext)
        fde20f.close()



if __name__ == '__main__':
    run()

