#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

# Post-Processing


def correctDate(date):
    str = ""
    if isDate(date):
        str = date
    else:
        # Ersetze "0" durch "."
        charArray = list(date)
        if charArray.__len__() >= 6:
            if charArray[2] == "0":
                charArray[2] = "."
            if charArray[5] == "0":
                charArray[5] = "."
            for char in charArray:
                str += char

    return str

def isDate(str):
    regexDate = re.compile(r"\b(\d{1,2}[-/:.]){1,2}\d{2,4}\b")
    if regexDate.match(str) is None:
        print "Fehler: Kein korrektes Datumsformat\n"
    else:
        print "korrektes Datumsformat\n"


def testIsDate():
    dates = ["10/03/2016", "10.03.2016", "10.03.16", "03-17", "32-13-14"]
    for date in dates:
        isDate(date)

if __name__ == "__main__":
    testIsDate()