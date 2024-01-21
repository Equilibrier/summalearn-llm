from pdf2docx import Converter

pdf_file = 'Curs SVT 01.pdf'
docx_file = 'target.docx'

# convert pdf to docx
cv = Converter(pdf_file)
cv.convert(docx_file, start=0, end=None)
cv.close()
