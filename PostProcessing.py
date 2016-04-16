import re

# Post-Processing


def correctDate(date):
    isDate(date)
    return date


def isDate(str):
    regexDate = re.compile(r"\b(\d{1,2}[-/:.]){1,2}\d{2,4}\b")
    if regexDate.match(str) is None:
        print "Fehler: Kein korrektes Datum"
    else:
        print "korrektes Datum"


def testIsDate():
    dates = ["10/03/2016", "10.03.2016", "10.03.16", "03-17", "32-13-14"]
    for date in dates:
        isDate(date)

if __name__ == "__main__":
    testIsDate()