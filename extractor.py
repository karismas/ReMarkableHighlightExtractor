import os
import sys
import cv2
import fitz
from PIL import Image, ImageChops
from pytesseract import pytesseract
from PyPDF2 import PdfReader

# Add ability to watch conversion page by page compared with diff
# Add ability to only get diff and not extraction
# Add ability to check between psm 1 and psm 6 and report difference as well as save diff for any problematic pages

def getHighlightedText(original, highlighted, output, fromPage, toPage, scale, psm, saveDiffs):

    path_to_tesseract = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract 

    if fromPage != 0:
        fromPage -= 1

    mat = fitz.Matrix(scale, scale)

    originalPages = fitz.open(original)
    highlightedPages = fitz.open(highlighted)

    with open(output, 'w') as file:

        file.write("")
        
        for i in range(fromPage, toPage):

            file.writelines(["\n\n      PAGE " + str(i + 1) + "\n\n"])
            
            originalPage = originalPages.load_page(i)
            highlightedPage = highlightedPages.load_page(i)

            originalPix = originalPage.get_pixmap(matrix=mat)
            highlightedPix = highlightedPage.get_pixmap(matrix=mat)

            originalPix.save('originalPage.jpg')
            highlightedPix.save('highlightedPage.jpg')

            originalImage = Image.open("originalPage.jpg")
            highlightedImage = Image.open("highlightedPage.jpg")

            diff = ImageChops.difference(originalImage, highlightedImage)
            print(diff.getbbox())

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
                file.writelines([text])

            file.write("")

    originalPages.close()
    highlightedPages.close()

    os.remove('originalPage.jpg')
    os.remove('highlightedPage.jpg')
    if not saveDiffs:
        os.remove('diff.jpg')

def main(args):

    original = "original.pdf"
    highlighted = "highlighted.pdf"
    output = "output.txt"
    fromPage = 0
    toPage = 0
    scale = 5
    psm = 1
    saveDiffs = False
    
    for i, arg in enumerate(args):
        if (arg == "--org"):
            original = args[i + 1]
        elif (arg == "--hl"):
            highlighted = args[i + 1]
        elif (arg == "--out"):
            output = args[i + 1]
        elif (arg == "--from"):
            fromPage = int(args[i + 1])
        elif (arg == "--to"):
            toPage = int(args[i + 1])
        elif (arg == "--scale"):
            scale = int(args[i + 1])
        elif (arg == "--psm"):
            psm = int(args[i + 1])
        elif (arg == "--diff"):
            saveDiffs = True if args[i + 1] == "t" else False

    if toPage == 0:
        
        reader = PdfReader(original)
        toPage = len(reader.pages)

    getHighlightedText(original, highlighted, output, fromPage, toPage, scale, psm, saveDiffs)

if __name__ == "__main__":
    main(sys.argv[1:])