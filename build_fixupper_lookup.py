from docx import Document
import re
    
# NU-mi mai trebuie nici asta si nici correct_uppercase_nouns.py (desi logica e brilianta, ideea mea si implementarea chatgpt + a mea :D) deci mai poate fi folosita -- read_pdf si read_doc imi stricau, de fapt, textul cu lower() iar nu chatgpt
    
if __name__ == "__main__":

    from lib_common import read_pdf, read_docx, replace_special_characters

    from os.path import abspath, dirname, join, basename, exists
    from os import listdir, remove

    from lib_common import text_to_pdf, replace_special_characters
    
    cdir = abspath(dirname(__file__))
    input_dir = join(cdir, 'input_pdfs')
    CACHE_UPPERMODEL_FILE = join(input_dir, "__upper_model_cache.txt")
    
    cached_upper_model = ""
    if exists(CACHE_UPPERMODEL_FILE):
        with open(CACHE_UPPERMODEL_FILE, "r") as f:
            cached_upper_model = f.read()
                    
    for filename in listdir(input_dir):
        fp = join(input_dir, filename)
        cached_upper_model += "\n" + replace_special_characters(read_docx(fp) if filename.endswith('.doc') or filename.endswith('.docx') else (read_pdf(fp) if filename.endswith('.pdf') else ""))
            
    with open(CACHE_UPPERMODEL_FILE, "w") as f:
        f.write(cached_upper_model)