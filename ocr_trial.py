import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np

_PYTESSERACT_INITIALIZED = False
def _initialize_pytesseract():
    global _PYTESSERACT_INITIALIZED
    if _PYTESSERACT_INITIALIZED:
        return
        
    # Dacă ai instalat Tesseract pe Windows, poate fi necesar să setezi calea către executabilul tesseract:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 
    
    _PYTESSERACT_INITIALIZED = True
    
def ocr_from_image_file(image_path):
    img = cv2.imread(image_path)
    text = ocr_image(img)
    return text

def ocr_image(img):
    _initialize_pytesseract()

    # Convertim imaginea în grayscale (necesar pentru unele tipuri de imagini pentru îmbunătățirea rezultatelor)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicăm OCR folosind pytesseract
    text = pytesseract.image_to_string(gray)
    return text


def ocr_pdf(pdf_path):
    # Convertim paginile PDF în imagini
    images = convert_from_path(pdf_path)

    # Inițializăm textul final cu un string gol
    final_text = ""

    # Iterăm prin fiecare imagine și aplicăm OCR
    for img in images:
        # Conversia din PIL Image la cv2 image (RGB to BGR)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        text = ocr_image(img)
        final_text += text + "\n"

    return final_text


if __name__ == "__main__":
    from sys import argv, exit
    if len(argv) <= 1:
        print("Un parametru obligatoriu: numele fisierului pdf/imagine la care sa faci ocr")
        exit(1)
        
    filen = argv[1]
    #import pdb; pdb.set_trace()
    # Testarea funcției
    text = ocr_pdf(filen) if filen.lower().endswith(".pdf") else ocr_from_image_file(filen)  # Înlocuiește 'documentul_tau.pdf' cu calea către fișierul tău PDF
    print(text)
