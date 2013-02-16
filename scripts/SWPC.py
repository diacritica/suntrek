#!/usr/bin/python
# -*- coding: utf-8 -*-

class SWPC:

    def __init__(self, SWMC):
        self.SWMC = SWMC

    def parseHTML(self, HTMLstringlist):
        self.sn = HTMLstring[1].strip().split(":")[1]
        self.issuetime = HTMLstring[2].strip().split(":")[1]
        self.alertlevel = HTMLstring[4].strip().split(":")[0]
        self.alert = HTMLstring[4].strip().split(":")[1]
