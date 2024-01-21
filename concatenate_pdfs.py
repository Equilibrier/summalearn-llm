import os

from PyPDF2 import PdfMerger
import zipfile

def concatenate_pdfs(directory, output_file):
    merger = PdfMerger()

    # Iterăm prin toate fișierele din director
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            # Deschidem fiecare fișier PDF și îl adăugăm la PDF-ul final
            print(f"concatenam fisierul {os.path.join(directory, filename)}")
            with open(os.path.join(directory, filename), "rb") as f:
                merger.append(f)

    # Scriem PDF-ul final
    with open(output_file, "wb") as output_pdf:
        merger.write(output_pdf)

    merger.close()
    print("Fișierul PDF a fost creat cu succes!")

def zip_files(file_list, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in file_list:
            # Folosește doar numele de bază al fișierului pentru arhivă
            zf.write(file, arcname=os.path.basename(file))
    print(f"am scris fisier zip {output_zip}")

if __name__ == "__main__":
    from os import remove, makedirs
    from os.path import join, abspath, dirname, exists
    from shutil import move
    from sys import argv, exit
    if len(argv) <= 1:
        print("Parametru obligatoriu: nume subdirector din output_pdfs, unde se gasesc pdf-urile input")
        exit(1)
        
    subdir = argv[1]
        
    cdir = abspath(dirname(__file__))
    input_dir = join(join(cdir, "output_pdfs"), subdir)
    #dump_dir = join(input_dir, "dump")
    #if not exists(dump_dir):
    #    makedirs(dump_dir)
    output_pdf_file = join(input_dir, f"{subdir}.pdf")
    output_zip_file = join(input_dir, f"{subdir}.zip")
    concatenate_pdfs(input_dir, output_pdf_file)
    zip_files([output_pdf_file], output_zip_file)
    remove(output_pdf_file)
    
    print(f"DONE, see {output_zip_file}")