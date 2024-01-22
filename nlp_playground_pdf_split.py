import fitz  # PyMuPDF

def extract_pages(pdf_path, start_page, end_page, output_path):
    doc = fitz.open(pdf_path)
    new_doc = fitz.open()

    for page_num in range(start_page - 1, end_page):
        page = doc.load_page(page_num)
        new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
        new_page.show_pdf_page(page.rect, doc, page_num)

    new_doc.save(output_path)
    new_doc.close()
    doc.close()

if __name__ == "__main__":

    import sys
    if len(sys.argv) <= 4:
        print("ERROR: four params required: input-pdf, output-pdf, start page, end page")
        sys.exit(1)
    #input_pdf = r'.\Mircea-Pacurariu-Istoria-Bisericii-Ortodoxe-Romane-Vol-2.pdf'
    input_pdf = sys.argv[1]
    #output_pdf='pagini_extrase.pdf'
    output_pdf = sys.argv[2]
    start_page = int(sys.argv[3])
    end_page = int(sys.argv[4])
        
    # Exemplu de utilizare
    extract_pages(input_pdf, start_page, end_page, output_pdf)
