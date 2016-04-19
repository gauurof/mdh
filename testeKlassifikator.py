#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import operator
import os
from PostProcessing import *

###################################################################################################
# Konstanten
MIN_CONTOUR_AREA = 100
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

# Test-Bilder 8 und 9 werden nicht korrekt erkannt.
# Test-Bild 2 wird im Post-Processing korrigiert, da Punkte nicht korrekt erkannt werden.
TEST_IMAGE = "TestBilder/testDatum.png"
CLASSIFIER = "klassifikationBenutzereingabe.txt"
TRAINED_IMAGES = "erkannteZeichen.txt"
###################################################################################################

class ContourWithData():

    npaContour = None
    boundingRect = None
    intRectX = 0
    intRectY = 0
    intRectWidth = 0
    intRectHeight = 0
    fltArea = 0.0

    def calculateRectTopLeftPointAndWidthAndHeight(self):
        [intX, intY, intWidth, intHeight] = self.boundingRect
        self.intRectX = intX
        self.intRectY = intY
        self.intRectWidth = intWidth
        self.intRectHeight = intHeight

    def checkIfContourIsValid(self):
        if self.fltArea < MIN_CONTOUR_AREA: return False
        return True

def main():
    allContoursWithData = []
    validContoursWithData = []

    try:
        npaClassifications = np.loadtxt(CLASSIFIER, np.float32)
    except:
        print "Fehler: Konnte Datei klassifikationBenutzereingabe.txt nicht öffnen!\n"
        os.system("pause")
        return

    try:
        npaFlattenedImages = np.loadtxt(TRAINED_IMAGES, np.float32)
    except:
        print "Fehler: Konnte Datei erkannteZeichen.txt nicht öffnen!\n"
        os.system("pause")
        return

    # 1D Numpy Array für KNN
    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))

    kNearest = cv2.ml.KNearest_create()
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)

    # Testbild einlesen
    imgTestingNumbers = cv2.imread(TEST_IMAGE)

    if imgTestingNumbers is None:
        print "Fehler: Konnte Bild nicht einlesen!\n"
        os.system("pause")
        return

    # Erstellung Grauwertbild und Rauschunterdrückung mit Gaussfilter
    imgGray = cv2.cvtColor(imgTestingNumbers, cv2.COLOR_BGR2GRAY)
    imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)

    # Erstellung Binärbild: Vordergrund weiß und Hintergrund schwarz
    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Erstellung einer Kopie des Binärbildes, da "findContours" Bild verändert.
    imgThreshCopy = imgThresh.copy()
    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Separiere Zeichen anhand der Konturen
    for npaContour in npaContours:
        contourWithData = ContourWithData()
        contourWithData.npaContour = npaContour
        contourWithData.boundingRect = cv2.boundingRect(contourWithData.npaContour)
        contourWithData.calculateRectTopLeftPointAndWidthAndHeight()
        contourWithData.fltArea = cv2.contourArea(contourWithData.npaContour)
        allContoursWithData.append(contourWithData)

    # überprüfung valider Konturen
    for contourWithData in allContoursWithData:
        if contourWithData.checkIfContourIsValid():
            validContoursWithData.append(contourWithData)

    # Sortieren von Links nach Rechts
    validContoursWithData.sort(key = operator.attrgetter("intRectX"))

    # Erkanntes Datum als String
    strFinalString = ""

    for contourWithData in validContoursWithData:

        cv2.rectangle(imgTestingNumbers, (contourWithData.intRectX, contourWithData.intRectY), (contourWithData.intRectX + contourWithData.intRectWidth, contourWithData.intRectY + contourWithData.intRectHeight), (0, 255, 0), 2)

        imgROI = imgThresh[contourWithData.intRectY : contourWithData.intRectY + contourWithData.intRectHeight, contourWithData.intRectX : contourWithData.intRectX + contourWithData.intRectWidth]

        # Anpassung der Größe des erkannten Zeichnes
        imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

        npaROIResized = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

        npaROIResized = np.float32(npaROIResized)

        # KNN Klassifikation zur Identifizierung
        retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)
        strCurrentChar = str(chr(int(npaResults[0][0])))

        #Anhängen des erkannten Zeichens zum Datum
        strFinalString = strFinalString + strCurrentChar
    # Überprüfung korrektes Datum (simples Post-Processing, kleine Fehlerkorrektur)
    correctedString = correctDate(strFinalString)

    print "Erkanntes Datum:    " + strFinalString
    print "Verbessertes Datum: " + correctedString
    cv2.imshow("Erkannte Zeichen im Bild", imgTestingNumbers)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return

if __name__ == "__main__":
    main()










