import os
import shutil
import fitz  # PyMuPDF
from PIL import Image
from subprocess import check_output

from lib_common import text_to_pdf


def is_image_pdf(file_path):
    doc = fitz.open(file_path)
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            base = doc.extract_image(xref)["image"]
            if base is None:
                return False
    return True
    

from os.path import abspath, dirname, join, basename, exists
cdir = abspath(dirname(__file__))
input_dir = join(cdir, 'input_pdfs')
CACHE_FILE = join(input_dir, "__process_cache.txt")

def process_available_files():
    os.system(f"python3 {join(cdir, 'summary3.py')}")
    os.system(f"python3 {join(cdir, 'text2fituica.py')}")

def process_pdfs_in_directory(input_pdfs_dir, output_txts_dir, output_pdfs_dir, set_file, pdftype_file):
    
    def create_subdir(root_dir, dir_name):
        set_dir = os.path.join(root_dir, dir_name)
        if not os.path.exists(set_dir):
            os.makedirs(set_dir)
        return set_dir
            
    def record_files(input_dir):
        file_set = []
        for filename in os.listdir(input_dir):
            if filename.endswith('.pdf') or filename.endswith(".doc") or filename.endswith(".docx"):
                full_path = os.path.join(input_dir, filename)
                file_set.append(full_path)
        return file_set
        
    # -1.1- Dacă există un fișier cu numele setului, citeste numele din el sau seteaza unul implicit, daca nu este
    set_name = 'ultimul_set'
    if os.path.exists(set_file):
        with open(set_file, 'r') as f:
            set_name = f.read().strip()
            
    # -1.2- Daca exista un fisier cu tipul pdf-ului, il citim si il folosim mai jos ca sa stim daca le ocr-izam pdf-urile sau nu; daca fisierul nu exista, atunci vom incerca sa facem selectia deterministic (cu un algoritm, dar care nu e prea prea bun, insa prioritizand ocr-izarea, va da rezultate bune, dar poate sa piarda timp aiurea, cand nu e cazul, deci fisierul de tip pdf e util...)
    pdftype_is_image = None
    if os.path.exists(pdftype_file):
        with open(pdftype_file, "r") as f:
            pdftype_is_image = f.read().strip().lower() == "image"
    
    # -2- Creează subdirectoare dump
    input_pdfs_dump_dir = create_subdir(input_pdfs_dir, set_name)
    output_txts_dump_dir = create_subdir(output_txts_dir, set_name)
    output_pdfs_dump_dir = create_subdir(output_pdfs_dir, set_name)

    # -3- Construiește cache-ul de fișiere procesate/spre-procesare
    input_pdfs_set = record_files(input_pdfs_dir)
    with open(CACHE_FILE, "a") as f:
        for fp in input_pdfs_set:
            f.write(basename(fp) + "\n")
        
    output_txts_set = []
    output_pdfs_set = []
    for file in input_pdfs_set:
        filen = basename(file)
        filen = filen[:filen.rfind(".")]
        output_txts_set.append(join(output_txts_dir, filen + ".txt"))
        output_pdfs_set.append(join(output_pdfs_dir, filen + ".pdf"))
    
    # -4.1- daca pdf-urile nu sunt editabile, intai le proceseaza cu ocr 
    for file in input_pdfs_set:
        #import pdb; pdb.set_trace()
        if (pdftype_is_image is not None and pdftype_is_image) or (pdftype_is_image is None and is_image_pdf(file)):
            text = check_output(f'python3 ocr_trial.py "{file}"', shell=True).decode("latin-1")
            text_to_pdf(text, file)
    
    # -4.2- apeleaza serviciile care proceseaza toate fisierele neprocesate inca
    process_available_files()
    
    # -5- dumpuie fisierele deja procesate (cele de intrare si cele de iesire, de asemenea)
    #import pdb; pdb.set_trace()
    for file in input_pdfs_set:
        dest_file = join(input_pdfs_dump_dir, basename(file))
        if exists(dest_file):
            os.remove(dest_file) # fisier procesat cu alta ocazie, il eliminam
        if not os.path.exists(file):
            print(f"Fisierul {file} trebuia sa existe, dar a fost sters/nu a fost generat ! Ignoram...")
            continue
        shutil.move(file, input_pdfs_dump_dir)
    for file in output_txts_set:
        dest_file = join(output_txts_dump_dir, basename(file))
        if exists(dest_file):
            os.remove(dest_file)
        if not os.path.exists(file):
            print(f"Fisierul {file} trebuia sa existe, dar a fost sters/nu a fost generat ! Ignoram...")
            continue
        shutil.move(file, output_txts_dump_dir)
    for file in output_pdfs_set:
        dest_file = join(output_pdfs_dump_dir, basename(file))
        if exists(dest_file):
            os.remove(dest_file)
        if not os.path.exists(file):
            print(f"Fisierul {file} trebuia sa existe, dar a fost sters/nu a fost generat ! Ignoram...")
            continue
        shutil.move(file, output_pdfs_dump_dir)
        
    # -6- creza o arhiva cu un singur fisier pdf, format din concatenarea fituicilor (raman si fisierele originare, nu-i problema...)
    os.system(f'python3 .\concatenate_pdfs.py "{set_name}"')
    print(f"vezi fisierul zip rezultat din subdirectorul '{set_name}'")


input_pdfs_dir = join(cdir, 'input_pdfs')
output_txts_dir = join(cdir, 'output_txts')
output_pdfs_dir = join(cdir, 'output_pdfs')
set_file = join(input_pdfs_dir, '__set.txt')
pdftype_file = join(input_pdfs_dir, '__pdf_type.txt')

if __name__ == "__main__":
    from time import sleep
    from os.path import exists, join, abspath, dirname
    
    cdir_ = abspath(dirname(__file__))
    INPUTS_DIR = join(cdir_, "input_pdfs")
    SECTIONS_BREAK_FILE = join(INPUTS_DIR, "__on_sections_break")
    SPLIT_MARKER_FILE = join(INPUTS_DIR, "__split")
    
    while True:
        # NU-mi mai mecanismul asta de restaurare uppercase fiindca read_pdf si read_doc imi stricau, de fapt, textul cu lower() iar nu chatgpt si am corectat deja
        '''print("Creaza modelul cache-uit pentru restaurare uppercase (dupa ce, uneori, chatgpt strica dandu-mi totul pe lowercase)...")
        os.system(f"python3 {join(cdir, 'build_fixupper_lookup.py')}")'''
        
        print("Daca am cerut (prin __split.txt) sa fie documentele sectionate, acum facem asta...")
        os.system(f"python3 {join(cdir, 'split_in_sections.py')}")
        
        if exists(SPLIT_MARKER_FILE) and exists(SECTIONS_BREAK_FILE):
            print(f"Pauza, va rog revizuiti sectiunile generate (le puteti sterge sau modifica denumirile ori continutul sau puteti anula intregul proces daca lucrurile nu au iesit deloc cum trebuiau), modificati ce se poate modifica, si daca totul e in regula, apasati tasta 'c' pentru a continua:")
            user_input = input()
            while user_input.lower() != 'c':
                print("Apasati tasta 'c' pentru a continua.")
                user_input = input()
        
        print(f"Procesam fisierele pdf din {input_pdfs_dir}...")
        process_pdfs_in_directory(input_pdfs_dir, output_txts_dir, output_pdfs_dir, set_file, pdftype_file)
        
        print("asteptam 5 secunde si reluam...")
        sleep(5)
        
