import os
import sys
import argparse

import numpy as np
from math import isclose

import cv2
import fitz
from PIL import Image, ImageChops
from pytesseract import pytesseract
from PyPDF2 import PdfReader

def getHighlightedText(highlighted, output, start, end, psm, numbering, display, blanks):

    #path_to_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    #pytesseract.tesseract_cmd = path_to_tesseract

    if start != 0 and numbering == 1:
        start -= 1

    scale = 5
    mat = fitz.Matrix(scale, scale)

    highlightedPages = fitz.open(highlighted)

    for i in range(start + (numbering - 1), end):
        highlightedPage = highlightedPages.load_page(i)
        highlightedPix = highlightedPage.get_pixmap(matrix=mat)
        highlightedPix.save('highlightedPage.jpg')

        img = cv2.imread('highlightedPage.jpg')
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        pinkRange = [(0, 140, 200), (255, 200, 255)]

        mask = cv2.inRange(hsv, pinkRange[0], pinkRange[1])
        target = cv2.bitwise_and(img, img, mask=mask)
        diff = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        contours, _ = cv2.findContours(diff, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        contourBounds = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 75:
                contourBounds.append((x, y, w, h))

        contourBounds = sorted(contourBounds, key=lambda val: (val[1], val[0]))

        text = ""
        for (index, bound) in enumerate(contourBounds):
            x = bound[0]
            y = bound[1]
            w = bound[2]
            h = bound[3]

            if index != 0:
                previousY = contourBounds[index - 1][1]
                if previousY == y:
                    text += " "
                else:
                    previousH = contourBounds[index - 1][3]
                    if y - (previousY + previousH) > h:
                        text += "\n\n"
                    else:
                        text += " "

            text += pytesseract.image_to_string(diff[y:y+h, x:x+w], config='--psm ' + str(psm))[:-1]
        
        if text != "":
            with open(output, 'a') as file:
                file.writelines(["\n# PAGE " + str(i + 1) + "\n\n"])
                file.writelines([text])
                file.write("")
           
            os.remove('highlightedPage.jpg')

            if display:
                cv2.imshow('image', img)
                cv2.waitKey(0)

        else:
            if display and blanks:
                cv2.imshow('image', img)
                cv2.waitKey(0)

    highlightedPages.close()

def main(args):

    end = args.end

    if end == 0:
        reader = PdfReader(args.highlighted)
        end = len(reader.pages)

    getHighlightedText(args.highlighted, args.output, args.start, end, args.psm, args.numbering, args.display, args.blanks)

def parse_arguments():

    parser = argparse.ArgumentParser(description="Extract highlights from a ReMarkable PDF.")
    parser.add_argument('highlighted', help="path of highlighted PDF")
    parser.add_argument('output', help="path of output file")
    parser.add_argument('-p', '--psm', help="psm for pytesseract to use", default=6)
    parser.add_argument('-s', '--start', help="extraction starting page", default=0, type=int)
    parser.add_argument('-e', '--end', help="extraction ending page", default=0, type=int)
    parser.add_argument('-n', '--numbering', help="the page relative to the PDF file where the page numbering actually starts at 1", default=1, type=int)
    parser.add_argument('-d', '--display', help="display the image of the page", action='store_true')
    parser.add_argument('-b', '--blanks', help="display the image of the page even if no highlights were detected", action='store_true')

    args = parser.parse_args()
    return args

if __name__ == "__main__":

    arguments = parse_arguments()
    main(arguments) 
