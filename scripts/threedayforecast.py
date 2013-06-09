#!/usr/bin/python                                                                                        
# -*- coding: utf-8 -*-
import json
import requests
import re

def run():

    #Retrieve and save source file
    r = requests.get("http://www.swpc.noaa.gov/ftpdir/latest/three_day_forecast.txt")
    i = open("output/threedayforecast.txt","w")
    i.write(r.content)
    i.close()

    #Parsing process, really ugly
    f = [line[:-1] for line in open("output/threedayforecast.txt","r").readlines()]
    
    fApos = f.index('A. NOAA Geomagnetic Activity Observation and Forecast')
    fBpos = f.index('B. NOAA Solar Radiation Activity Observation and Forecast')
    fCpos = f.index('C. NOAA Radio Blackout Activity and Forecast')
    
    cleanlines = []

    for line in f[fApos+10:fApos+18]:
        cleanlines.append(re.sub(r'\(.*\)','',line))

    hours=[line.split() for line in cleanlines]

    print(hours)
    
    hoursday1 = [(data[0],data[1]) for data in hours]
    hoursday2 = [(data[0],data[2]) for data in hours]
    hoursday3 = [(data[0],data[3]) for data in hours]
    
    geomagnetic = {"title":f[fApos][3:], "expected":"".join(f[fApos+4:fApos+6]),
                   "day1":{"title":"".join(f[fApos+9].split()[0:2]),
                           "hours":hoursday1},
                   "day2":{"title":"".join(f[fApos+9].split()[2:4]),
                           "hours":hoursday2},
                   "day3":{"title":"".join(f[fApos+9].split()[4:6]),
                           "hours":hoursday3},
                   "rationale":" ".join(f[fApos+19:fBpos-1]).split(":")[1].strip(),
    }
   

    endhoursB = f.index("",fBpos+8)
    
    hoursB = []
    for line in f[fBpos+8:endhoursB]:
        cleanline = line.split("   ")
        cleanline2 = [cleanline[0]] + [token for token in cleanline[1:] if token != ""] #I hate NOAA syntax
        hoursB.append(cleanline2)

#    hoursB = [line.split("   ") for line in f[fBpos+8:endhoursB]]

    print(hoursB)

    hoursBday1 = [(data[0],data[1][:-1]) for data in hoursB]
    hoursBday2 = [(data[0],data[2][:-1]) for data in hoursB]
    hoursBday3 = [(data[0],data[3][:-1]) for data in hoursB]

    print("...............")
    print(hoursBday1)
    print(hoursBday2)
    print(hoursBday3)

    radiation = {"title": f[fBpos][3:],
                 "day1":{"title":"".join(f[fBpos+7].split()[0:2]),
                         "cat":hoursBday1},
                 "day2":{"title":"".join(f[fBpos+7].split()[2:4]),
                         "cat":hoursBday2},
                 "day3":{"title":"".join(f[fBpos+7].split()[4:6]),
                         "cat":hoursBday3},
                 "rationale":" ".join(f[endhoursB+1:fCpos-1]).split(":")[1].strip(),
    }
             


    NUMTOKEN = 6 
    #sadly, we have to check if the file has two lines after C. section and not the usual one
    if f.index("",fCpos+3)!="\n":
        NUMTOKEN = 7
        print NUMTOKEN

    endhoursC = f.index("",fCpos+NUMTOKEN+1)

    hoursCprev = [line.split() for line in f[fCpos+NUMTOKEN+1:endhoursC]]
    print hoursCprev
    hoursC = [(" ".join(l[:-3]),l[-3],l[-2],l[-1]) for l in hoursCprev]
    print hoursC

    hoursCday1 = [(data[0],data[1][:-1]) for data in hoursC]
    hoursCday2 = [(data[0],data[2][:-1]) for data in hoursC]
    hoursCday3 = [(data[0],data[3][:-1]) for data in hoursC]
    print hoursCday1
    print hoursCday2
    print hoursCday3

    radioblackout = {"title": f[fCpos][3:],
                     "day1":{"title":"".join(f[fCpos+NUMTOKEN].split()[0:2]),
                             "cat":hoursCday1},
                     "day2":{"title":"".join(f[fCpos+NUMTOKEN].split()[2:4]),
                             "cat":hoursCday2},
                     "day3":{"title":"".join(f[fCpos+NUMTOKEN].split()[4:6]),
                             "cat":hoursCday3},
                     "rationale":" ".join(f[endhoursC+1:]).split(":")[1].strip(),
                 }
               

    #JSON FILES CREATION
    
    #GEOMAGNETIC
    geomagneticdict = {

        "fitType": "line",
        "label": "Kp Index Breakdown",
        "legendEntry": True,
        "markers": {
            "type": "circle",
            "visible": True
        },
        "data":{
            "x":[d[0] for d in geomagnetic["day1"]["hours"]] + [d[0] for d in geomagnetic["day2"]["hours"]] + [d[0] for d in geomagnetic["day3"]["hours"]],
            "y":[int(d[1]) for d in geomagnetic["day1"]["hours"]] + [int(d[1]) for d in geomagnetic["day2"]["hours"]] + [int(d[1]) for d in geomagnetic["day3"]["hours"]]
        },
        

        "expected": geomagnetic["expected"],
        "rationale": geomagnetic["rationale"]
    }

    tdff = open("output/threedayforecastg.json","w")

    jsontext = json.dumps(geomagneticdict, sort_keys=True,
                      indent=4, separators=(',', ': '))
    tdff.write(jsontext)
    tdff.close()



    #RADIATION
    categories = [cat[0] for cat in radiation["day1"]["cat"]]
    catnumber = len(categories)
    tdff = open("output/threedayforecastr.json","w")
    if catnumber > 1:
        jsonappend = ","
    else:
        jsonappend = ""

    for i in range(catnumber):

        radiationdict = {
            "fitType": "line",
            "label": categories[i]+" (% prob)",
            "legendEntry": True,
            "markers": {
                "type": "circle",
                "visible": True
            },
            
            "data":{
                "x":[radiation["day1"]["title"] , radiation["day2"]["title"] , radiation["day3"]["title"]],
                "y":[int(radiation["day1"]["cat"][i][1]), int(radiation["day2"]["cat"][i][1]), int(radiation["day3"]["cat"][i][1])]
            },
            "rationale": radiation["rationale"]
        }
        
        jsontext = json.dumps(radiationdict, sort_keys=True,
                              indent=4, separators=(',', ': '))
        tdff.write(jsontext+jsonappend)
        
    tdff.close()

    #RADIOBLACKOUT
    categories = [cat[0] for cat in radioblackout["day1"]["cat"]]
    catnumber = len(categories)
    tdff = open("output/threedayforecastrb.json","w")
    if catnumber > 1:
        jsonappend = ","
    else:
        jsonappend = ""

    for i in range(catnumber):

        radioblackoutdict = {

            "fitType": "line",
            "label": categories[i]+" (% prob)",
            "legendEntry": True,
            "markers": {
                "type": "circle",
                "visible": True
            },
            
            "data":{
                "x":[radioblackout["day1"]["title"] , radioblackout["day2"]["title"] , radioblackout["day3"]["title"]],
                "y":[int(radioblackout["day1"]["cat"][i][1]), int(radioblackout["day2"]["cat"][i][1]), int(radioblackout["day3"]["cat"][i][1])]
            },
            "rationale": radioblackout["rationale"],
        }
        
    
        jsontext = json.dumps(radioblackoutdict, sort_keys=True,
                          indent=4, separators=(',', ': '))
        tdff.write(jsontext+jsonappend)

    
    tdff.close()


if __name__ == '__main__':
#    pass
    run()
