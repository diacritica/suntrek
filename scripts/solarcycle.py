#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import collections
import datetime
import json

import settings

#today = datetime.date.today() fixme with zfill
urlwithfile = "http://www.swpc.noaa.gov/ftpdir/weekly/RecentIndices.txt"
urlwithfile2 = "http://www.swpc.noaa.gov/ftpdir/weekly/Predict.txt"
"""
:Recent_Solar_Indices: RecentIndices.txt
:Created: 2013 Feb 04 0833 UTC
# Prepared by the U.S. Dept. of Commerce, NOAA, Space Weather Prediction Center (SWPC).
# Please send comments and suggestions to swpc.webmaster@noaa.gov
#
# Source SWO: SWPC Space Weather Operations (SWO).
# Source RI: S.I.D.C. Brussels International Sunspot Number.
# Source 10.7cm radio flux values (sfu): Penticton, B.C., Canada.
# 
# Source Ap: GeoForschungsZentrum, Postdam, Germany
#            Prior to January 1997, Institut fur Geophysik, Gottingen, Germany
# Source Ap for final month is NOAA/SWPC estimated Ap.
#
# Data not yet available or not calculable: -1.0
#
# Values for most recent 6 months are considered preliminary. 
# Final values from National Geophysical Data Center www.ngdc.noaa.gov
#
#                               Recent Solar Indices
#                         of Observed Monthly Mean Values
#
#       -----------Sunspot Numbers--------- ----Radio Flux---  ---Geomagnetic---
#       ---Observed---- Ratio   --Smoothed- Observed Smoothed  Observed Smoothed
# YR MO    SWO     RI   RI/SW    SWO   RI     10.7cm  10.7cm      Ap       Ap
#-------------------------------------------------------------------------------
1991 01   213.5   136.9  0.64   220.5 147.6    229.4    205.5         8     17.4
1991 02   270.2   167.5  0.62   221.5 147.6    243.0    206.3        10     18.4
1991 03   227.9   141.9  0.62   220.7 146.6    230.0    205.9        27     19.1
1991 04   215.9   140.0  0.65   220.7 146.5    198.8    206.8        17     20.0
1991 05   182.5   121.3  0.66   219.6 145.5    190.3    207.1        18     21.7
1991 06   231.8   169.7  0.73   218.9 145.2    206.8    207.4        44     23.0
1991 07   245.7   173.7  0.71   219.5 146.3    212.0    207.7        27     23.6
1991 08   251.5   176.3  0.70   218.3 146.6    210.3    206.8        30     24.7
1991 09   185.8   125.3  0.67   214.2 144.9    180.6    203.9        20     25.0
1991 10   220.1   144.1  0.65   208.4 141.7    201.3    199.7        31     24.3
1991 11   169.0   108.2  0.64   202.2 138.1    172.0    195.4        33     24.1

"""

def run():

    if settings.TEST == True:
        pass

    else:

        r = requests.get(urlwithfile)
        with open("output/RecentIndices.txt","w") as fdurl:
            fdurl.write(r.text)
            fdurl.close()

        r2 = requests.get(urlwithfile2)
        with open("output/Predict.txt","w") as fdurl2:
            fdurl2.write(r2.text)
            fdurl2.close()

        particle_map = {}

        fdfile = open("output/RecentIndices.txt","r")
        fdfile2 = open("output/Predict.txt","r")

        fdoscf = open("output/observedsolarcycle.json","w")
        fdsscf = open("output/smoothedsolarcycle.json","w")

        fdpsscf = open("output/predictedsmoothedsolarcycle.json","w")
        
        sunspotsdatelist = []
        observedsunspotslist = []
        smoothedsunspotslist = []

        predictedsunspotsdatelist = []
        predictedsunspotslist = []
        predictedsmoothedsunspotslist = []

        for line in fdfile2:
            values = line.strip().split()
            if len(values) == 8:
                YR,MO,SPR,SH,SL,RPR,RH,RL = values
                predictedsunspotdate = "-".join([YR,MO])
                if YR != "2012":
                    if MO == "01":
                        predictedsunspotsdatelist.append(YR[2:])
                    else:
                        predictedsunspotsdatelist.append(".")
                        try:
                            predictedsmoothedsunspotslist.append(float(SPR))
                        except:
                            pass


        for line in fdfile:
            values = line.strip().split()
            if len(values) == 11:
                YR,MO,OSWO,ORI,ORISW,SSWO,SRI,RO,RS,GO,GS = values
                sunspotdate = "-".join([YR,MO])
                
                if MO == "01":
                    sunspotsdatelist.append(YR[2:])
                else:
                    sunspotsdatelist.append(".")

                observedsunspotslist.append(float(OSWO))
                smoothedsunspotslist.append(float(SSWO))

        

        smoothedsunspotslist = smoothedsunspotslist[:-6]
        observedsunspotsdict = {"label":"Monthly values","legendEntry":True, "fitType": "line",
                   "data" : {
                "x" : sunspotsdatelist + predictedsunspotsdatelist,
                "y" : observedsunspotslist,                
                },
                   "markers" : {
                "visible" : True, "type" : "circle",
                },

                   }
        jsontext = json.dumps(observedsunspotsdict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fdoscf.write(jsontext)
        fdoscf.close()


        smoothedsunspotsdict = {"label":"Smoothed Monthly values","legendEntry":True, "fitType": "spline",
                   "data" : {
                "x" : sunspotsdatelist + predictedsunspotsdatelist,
                "y" : smoothedsunspotslist,                
                },
                   "markers" : {
                "visible" : True, "type" : "circle",
                },

                   }
        jsontext = json.dumps(smoothedsunspotsdict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fdsscf.write(jsontext)
        fdsscf.close()


        predictedsunspotsdict = {"label":"Predicted Monthly values","legendEntry":True, "fitType": "bezier",
                   "data" : {
                "x" : sunspotsdatelist + predictedsunspotsdatelist,
                "y" : smoothedsunspotslist + predictedsmoothedsunspotslist,                
                },
                   "markers" : {
                "visible" : False, "type" : "circle",
                },

                   }
        jsontext = json.dumps(predictedsunspotsdict, sort_keys=True,
                              indent=4, separators=(',', ': '))

        fdpsscf.write(jsontext)
        fdpsscf.close()


if __name__ == '__main__':
    run()

