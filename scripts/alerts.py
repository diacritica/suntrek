#!/usr/bin/python                                                                                        
# -*- coding: utf-8 -*-
import json
import requests


r = requests.get("http://www.swpc.noaa.gov/alerts/archive/current_month.html")
i = open("output/current_month.html","w")
i.write(r.content)
i.close()
print("current_month.html saved")

alerts = [line[:-1] for line in open("output/current_month.html","r").readlines()]

pos = alerts.index("<hr><p>")
alertsList = []

try:
    while True:
        pos = alerts.index("<hr><p>",pos)
        SWMC = alerts[pos+1].split(":")[1][:-4].strip()
        SN = alerts[pos+2].split(":")[1][:-4].strip()
        ISSUETIME = alerts[pos+3].split(":")[1][:-4].strip()
        ALERTTYPE = alerts[pos+5].split(":")[0][3:].strip()
        ALERTMESSAGE = alerts[pos+5].split(":")[1][:-4].strip()
        
        oldpos = pos
        pos = alerts.index("<hr><p>",oldpos+1)
        RAWPAYLOAD = "".join(alerts[oldpos+6:pos])
        PAYLOAD = []
        PLLINES = RAWPAYLOAD.split("<br>")[:-1]
     
        for line in PLLINES:
            try:
                if line.count(":")>0:
                    HEADER, CONTENT = line.split(":")
                elif line.count("-")>0:
                    HEADER, CONTENT = line.split("-")
                    
                PAYLOAD.append((HEADER.strip(),CONTENT.strip()))

            except:
                pass

        alertDict = {
            "SWMC":SWMC,
            "SN":SN,
            "ISSUETIME":ISSUETIME,
            "ALERTTYPE":ALERTTYPE,
            "ALERTMESSAGE":ALERTMESSAGE,
            "PAYLOAD":PAYLOAD,
            "RAWPAYLOAD":RAWPAYLOAD,
            }
        
        alertsList.append(alertDict)

except:
    pass

alertsfile = open("output/alerts.json","w")
jsontext = json.dumps(alertsList, sort_keys=True,
                      indent=4, separators=(',', ': '))

alertsfile.write(jsontext)
alertsfile.close()



