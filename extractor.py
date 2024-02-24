import os
import sys
import argparse

import cv2
import fitz
from PIL import Image, ImageChops
from pytesseract import pytesseract
from PyPDF2 import PdfReader

# Add ability to watch conversion page by page compared with diff
# Add ability to only get diff and not extraction
# Add ability to check between psm 1 and psm 6 and report difference as well as save diff for any problematic pages

def getHighlightedText(original, highlighted, output, fromPage, toPage, scale, psm, saveDiffs, pauseDiffs):

    #path_to_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    #pytesseract.tesseract_cmd = path_to_tesseract 

    if fromPage != 0:
        fromPage -= 1

    mat = fitz.Matrix(scale, scale)

    originalPages = fitz.open(original)
    highlightedPages = fitz.open(highlighted)

    for i in range(fromPage, toPage):

        originalPage = originalPages.load_page(i)
        highlightedPage = highlightedPages.load_page(i)

        originalPix = originalPage.get_pixmap(matrix=mat)
        highlightedPix = highlightedPage.get_pixmap(matrix=mat)

        originalPix.save('originalPage.jpg')
        highlightedPix.save('highlightedPage.jpg')

        originalImage = Image.open("originalPage.jpg")
        highlightedImage = Image.open("highlightedPage.jpg")

        diff = ImageChops.difference(originalImage, highlightedImage)

        diffName = ''
        if saveDiffs:
            diffName = 'diff' + str(i + 1) + '.jpg'
        else:
            diffName = 'diff.jpg'

        diff.save(diffName, 'JPEG')

        diff = cv2.imread(diffName)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(diff, config='--psm ' + str(psm))
        text = text[:-1]
        
        if text != "":
            with open(output, 'a') as file:
                file.writelines(["\n\n      PAGE " + str(i + 1) + "\n\n"])
                file.writelines([text])
                file.write("")

        shownImage = cv2.imread('highlightedPage.jpg')
        cv2.imshow('image', shownImage)
        cv2.waitKey(0)

    originalPages.close()
    highlightedPages.close()

    os.remove('originalPage.jpg')
    os.remove('highlightedPage.jpg')
    if not saveDiffs:
        os.remove('diff.jpg')

def main(args):

    toPage = args.toPage

    if toPage == 0:
        
        reader = PdfReader(args.original)
        toPage = len(reader.pages)

    getHighlightedText(args.original, args.highlighted, args.output, args.fromPage, toPage, args.scale, args.psm, False, args.diff)

def parse_arguments():

    parser = argparse.ArgumentParser(description="Extract highlights from a ReMarkable PDF.")
    parser.add_argument('original', help="path of original PDF")
    parser.add_argument('highlighted', help="path of highlighted PDF")
    parser.add_argument('output', help="path of output file")
    parser.add_argument('-s', '--scale', help="scale of the fitz matrix", default=5)
    parser.add_argument('-p', '--psm', help="psm for pytesseract to use", default=1)
    parser.add_argument('-f', '--fromPage', help="extraction starting page", default=0, type=int)
    parser.add_argument('-t', '--toPage', help="extraction ending page", default=0, type=int)
    parser.add_argument('-d', '--diff', help="display the image of the diff between the original and highlighted images", default=True)

    args = parser.parse_args()
    return args

if __name__ == "__main__":

    arguments = parse_arguments()
    main(arguments) 

#main(sys.argv[1:])
