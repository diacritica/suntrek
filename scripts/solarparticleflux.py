#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import collections
import datetime
import json

import settings

urlwithfile = "http://www.swpc.noaa.gov/ftpdir/lists/particle/Gp_part_5m.txt"

"""
:Data_list: Gs_part_5m.txt
:Created: 2013 Feb 16 1211 UTC
# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center
# Please send comments and suggestions to SWPC.Webmaster@noaa.gov 
# 
# Label: P > 1 = Particles at >1 Mev
# Label: P > 5 = Particles at >5 Mev
# Label: P >10 = Particles at >10 Mev
# Label: P >30 = Particles at >30 Mev
# Label: P >50 = Particles at >50 Mev
# Label: P>100 = Particles at >100 Mev
# Label: E>0.8 = Electrons at >0.8 Mev
# Label: E>2.0 = Electrons at >2.0 Mev
# Label: E>4.0 = Electrons at >4.0 Mev
# Units: Particles = Protons/cm2-s-sr
# Units: Electrons = Electrons/cm2-s-sr
# Source: GOES-15
# Location: W135
# Missing data: -1.00e+05
#
#                      5-minute  GOES-15 Solar Particle and Electron Flux
#
#                 Modified Seconds
# UTC Date  Time   Julian  of the
# YR MO DA  HHMM    Day     Day     P > 1     P > 5     P >10     P >30     P >50     P>100     E>0.8     E>2.0     E>4.0
#-------------------------------------------------------------------------------------------------------------------------
2013 02 16  1010   56339  36600   7.47e-01  2.48e-01  2.21e-01  6.91e-02  5.95e-02  4.07e-02  1.07e+04  3.38e+01 -1.00e+05
2013 02 16  1015   56339  36900   6.97e-01  1.15e-01  8.82e-02  4.85e-02  3.88e-02  2.00e-02  1.19e+04  3.87e+01 -1.00e+05
2013 02 16  1020   56339  37200   1.36e+00  2.62e-01  1.39e-01  8.03e-02  4.43e-02  2.00e-02  1.30e+04  3.81e+01 -1.00e+05
2013 02 16  1025   56339  37500   7.57e-01  1.65e-01  1.38e-01  7.04e-02  6.07e-02  2.71e-02  1.34e+04  4.82e+01 -1.00e+05
2013 02 16  1030   56339  37800   7.66e-01  1.27e-01  1.00e-01  6.00e-02  4.14e-02  2.00e-02  1.47e+04  4.72e+01 -1.00e+05
"""

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

        P100dict = {"label":"P>100MeV","legendEntry":True, "fitType": "line",
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

