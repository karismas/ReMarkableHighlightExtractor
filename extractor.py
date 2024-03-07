import os
import sys
import argparse

import numpy as np

import cv2
import fitz
from PIL import Image, ImageChops
from pytesseract import pytesseract
from PyPDF2 import PdfReader

def getHighlightedText(highlighted, output, fromPage, toPage, scale, psm, pauseDiffs):

    #path_to_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    #pytesseract.tesseract_cmd = path_to_tesseract 

    if fromPage != 0:
        fromPage -= 1

    mat = fitz.Matrix(scale, scale)

    highlightedPages = fitz.open(highlighted)

    for i in range(fromPage, toPage):

        highlightedPage = highlightedPages.load_page(i)
        highlightedPix = highlightedPage.get_pixmap(matrix=mat)
        highlightedPix.save('highlightedPage.jpg')

        img = cv2.imread('highlightedPage.jpg')
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0, 140, 200), (255, 200, 255))
        target = cv2.bitwise_and(img, img, mask=mask)
        diff = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(diff, config='--psm ' + str(psm))
        text = text[:-1]
        
        if text != "":
            with open(output, 'a') as file:
                file.writelines(["\n# PAGE " + str(i + 1) + "\n\n"])
                file.writelines([text])
                file.write("")

        shownImage = cv2.imread('highlightedPage.jpg')
        cv2.imshow('image', shownImage)
        cv2.waitKey(0)

    highlightedPages.close()

    os.remove('highlightedPage.jpg')
    if not saveDiffs:
        os.remove('diff.jpg')

def main(args):

    toPage = args.toPage

    if toPage == 0:
        
        reader = PdfReader(args.highlighted)
        toPage = len(reader.pages)

    getHighlightedText(args.highlighted, args.output, args.fromPage, toPage, args.scale, args.psm, args.diff)

def parse_arguments():

    parser = argparse.ArgumentParser(description="Extract highlights from a ReMarkable PDF.")
    parser.add_argument('highlighted', help="path of highlighted PDF")
    parser.add_argument('output', help="path of output file")
    parser.add_argument('-s', '--scale', help="scale of the fitz matrix", default=5)
    parser.add_argument('-p', '--psm', help="psm for pytesseract to use", default=6)
    parser.add_argument('-f', '--fromPage', help="extraction starting page", default=0, type=int)
    parser.add_argument('-t', '--toPage', help="extraction ending page", default=0, type=int)
    parser.add_argument('-d', '--diff', help="display the image of the diff between the original and highlighted images", default=True)

    args = parser.parse_args()
    return args

if __name__ == "__main__":

    arguments = parse_arguments()
    main(arguments) 
