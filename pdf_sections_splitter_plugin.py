import fitz  # PyMuPDF
import os

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

def split_pdf(pdf_path, instructions_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(instructions_file, 'r') as file:
        for line in file:
            start_page, end_page, label = line.strip().split(',')
            output_path = os.path.join(output_dir, f"{label}.pdf")
            extract_pages(pdf_path, int(start_page), int(end_page), output_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: script.py <PDF file> <Instructions file> <Output directory>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    instructions_file = sys.argv[2]
    output_directory = sys.argv[3]

    split_pdf(pdf_file, instructions_file, output_directory)
