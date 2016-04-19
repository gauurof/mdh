#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import cv2
import os

###################################################################################################
# Konstanten
MIN_CONTOUR_AREA = 100
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30
###################################################################################################

def main():
    # Bild, mit dem Klassifikator trainert wird
    imgTrainingNumbers = cv2.imread("TrainingsBilder/DatumVorlage.PNG")

    if imgTrainingNumbers is None:
        print "Fehler: Konnte Bild nicht einlesen!\n"
        os.system("pause")
        return -1

    # Erstellung Grauwertbild und Rauschunterdrückung mit Gaussfilter
    imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)
    imgBlurred = cv2.GaussianBlur(imgGray, (5, 5), 0)

    # Erstellung Binärbild: Vordergrund weiß und Hintergrund schwarz
    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    cv2.imshow("imgThresh", imgThresh)
    # Erstellung einer Kopie des Binärbildes, da "findContours" Bild verändert.
    imgThreshCopy = imgThresh.copy()
    imgContours, npaContours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    npaFlattenedImages =  np.empty((0, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))

    # Array für Benutzereingabe zu den erkannten Zeichen
    intClassifications = []
    intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), ord('/'), ord('.')]

    # Alle gefundenen Konturen werden mit einem roten Rechteck gekennzeichnet
    for npaContour in npaContours:
        if cv2.contourArea(npaContour) > MIN_CONTOUR_AREA:
            [intX, intY, intW, intH] = cv2.boundingRect(npaContour)

            # Zeichne rotes Rechteck
            cv2.rectangle(imgTrainingNumbers, (intX, intY), (intX+intW, intY+intH), (0, 0, 255), 2)

            # Gefundenes Zeichnen ausscheinden und Größe anpassen
            imgROI = imgThresh[intY:intY+intH, intX:intX+intW]
            imgROIResized = cv2.resize(imgROI, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

            cv2.imshow("Gefundenes Zeichen", imgROI)
            cv2.imshow("Gefundenes, angepasstes Zeichen", imgROIResized)
            # Zeige das gefundene Zeichen im Originalbild mit rotem Rechteck
            cv2.imshow("training_numbers.png", imgTrainingNumbers)

            # Warten auf Usereingabe für erkanntes Zeichen
            intChar = cv2.waitKey(0)
            if intChar == 27:
                sys.exit()
            elif intChar in intValidChars:
                # Benutzereingabe in Array speichern
                intClassifications.append(intChar)

                npaFlattenedImage = imgROIResized.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT))
                npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)

    fltClassifications = np.array(intClassifications, np.float32)
    npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))

    print "Lernphase abeschlossen!\n"

    np.savetxt("klassifikationBenutzereingabe1.txt", npaClassifications)
    np.savetxt("erkannteZeichen1.txt", npaFlattenedImages)

    cv2.destroyAllWindows()

    return

if __name__ == "__main__":
    main()




