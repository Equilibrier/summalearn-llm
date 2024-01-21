from docx import Document
import re


def _extract_sections(file_path):

    def first_nonempty_run_is_bold(paragraph):
            for run in paragraph.runs:
                if len(run.text.strip()) > 0:  # Daca run.text.strip() este ne-gol
                    return run.bold is True  # Verifica daca primul "run" ne-gol este boldat
            return False  # Daca nu exista niciun "run" ne-gol, returneaza False

    doc = Document(file_path)
    sections = {}
    current_section = ""
    section_text = ""

    for paragraph in doc.paragraphs:
        if len(paragraph.text.strip()) <= 0:
            continue
        
        # Criterii pentru identificarea unui titlu nou        
        if paragraph.style.name in ['Heading 1', 'Heading 2', 'Heading 3'] or first_nonempty_run_is_bold(paragraph) or paragraph.alignment == 1:  # Presupunem ca 1 este pentru centrare
            
            #import pdb; pdb.set_trace()
            #print(f"paragraf selectat: {paragraph.text[:20]}")
            
            # Verificam daca este un titlu fals
            if any(run.bold is False and len(run.text.strip()) > 0 for run in paragraph.runs):
                section_text += ' ' + paragraph.text  # Daca este fals, adaugam textul la sectiunea curenta
            else:
                if current_section != "":
                    # Salvam textul sectiunii anterioare
                    sections[current_section] = section_text.strip()

                # Titlul curent
                current_section = paragraph.text.strip()

                # Resetam textul sectiunii
                section_text = ""

        elif current_section != "":
            section_text += ' ' + paragraph.text

    # Salvam ultima sectiune
    if current_section != "":
        sections[current_section] = section_text.strip()

    return sections


def _pp_combine_empty_titles(sections):
    from fuzzywuzzy import fuzz

    def remove_common_words(title):
        common_words = ["și", "sau", "de", "la", "că", "cu", "în", "pe", "despre", "fără", "pentru"]  # etc.
        words = title.split()
        words = [word for word in words if word.lower() not in common_words]
        return ' '.join(words)

    def remove_duplicate_words(title):
        words = title.split()
        seen_words = set()
        unique_words = []
        for word in words:
            if word.lower() not in seen_words:
                seen_words.add(word.lower())
                unique_words.append(word)
        return ' '.join(unique_words)

    def remove_specific_words(title, words_to_remove):
        words = title.split()
        cleaned_words = [word for word in words if not any(fuzz.ratio(word.lower(), remove_word.lower()) > 70 for remove_word in words_to_remove)]
        return ' '.join(cleaned_words)

    def remove_number_groups(title):
        return re.sub(r'\b(\d+[\.,#-])*[\.,#-]?\d+\b', '', title)

    def shorten_title(title, max_words):
        words = title.split()
        short_title = ' '.join(words[:max_words]) 
        return short_title
        

    #title = "Cursul 01 Cărțile istorice ale Vechiului Testament, Legământul, Teocrația. Cărțile istorice ale Vechiului Testament."
    #print(title)
    #print(shorten_title(remove_common_words(remove_duplicate_words(remove_numbers(remove_specific_words(title, ["curs", "al"])))), 6))


    from collections import OrderedDict

    sections = list(sections.items())
    new_sections = OrderedDict()
            
    i = 0
    while i < len(sections):
        if len(sections[i][1].strip()) <= 0:
            new_title = ""
            while len(sections[i][1].strip()) <= 0:
                new_title += sections[i][0] + " "
                i += 1
            new_title += sections[i][0]
            new_title = shorten_title(remove_common_words(remove_duplicate_words(remove_number_groups(remove_specific_words(new_title, ["curs", "al"])))), 6)
            new_sections[new_title] = sections[i][1]
        else:
            new_sections[sections[i][0]] = sections[i][1]
        i += 1

    return new_sections
    
def _pp_fix_sublists(sections):

    from collections import OrderedDict
    import re
    def match_bullet_consecutive_lines(line1, line2):
        # Identificăm prefixul pentru primul string
        prefix1 = re.match(r'(-|\*|\+|\d+[\.\) ])', line1)
        prefix1 = prefix1.group() if prefix1 else None

        # Identificăm prefixul pentru al doilea string
        prefix2 = re.match(r'(-|\*|\+|\d+[\.\) ])', line2)
        prefix2 = prefix2.group() if prefix2 else None

        # Verificăm dacă ambele stringuri au prefixuri numerice
        if prefix1 and prefix2 and prefix1[:-1].isdigit() and prefix2[:-1].isdigit():
            return int(prefix1[:-1]) + 1 == int(prefix2[:-1])

        # Altfel, comparăm direct prefixurile
        return prefix1 == prefix2
        
    sections = list(sections.items())
    new_sections = OrderedDict()

    i = 0
    while i < len(sections):
        title, content = sections[i]
        
        if content.endswith(":") and i < len(sections)-1 and len(sections[i+1][1].strip()) <= 0:
            list_content = ""
            i += 1
            while i < len(sections) and len(sections[i][1].strip()) == 0:
                list_content += "\n" + sections[i][0]
                i += 1
            if match_bullet_consecutive_lines(sections[i-1][0], sections[i][0]):
                list_content += "\n" + sections[i][0] + "\n" + sections[i][1]
            else:
                i -= 1
            new_sections[title] = content + list_content
            
        else:
            new_sections[title] = content

        i += 1

    return new_sections
    
if __name__ == "__main__":
    from pdf2docx import Converter
    from reportlab.pdfgen import canvas

    from os.path import abspath, dirname, join, basename, exists
    from os import listdir, remove
    import re
    import unicodedata
    import string
    
    def sanitize_filename(filename):
        import string

        def more_sanitization(title, replace_with='_'):
            # Înlocuirea spațiilor albe la începutul și sfârșitul titlului
            sanitized = title.strip()
            # Înlocuirea tuturor caracterelor speciale și de control cu un anumit caracter
            allowed_chars = set(string.ascii_letters + string.digits + '-_. ')
            sanitized = ''.join(c if c in allowed_chars else replace_with for c in sanitized)
            # Verificarea dacă titlul nu depășește o lungime maximă permisă
            max_length = 255  # lungimea maximă permisă pentru numele de fișiere în majoritatea sistemelor de operare
            if len(sanitized) > max_length:
                print(f"Avertisment: '{title}' este prea lung și va fi trunchiat.")
                sanitized = sanitized[:max_length]
            return sanitized
        
        # Înlocuiește diacriticele cu caractere echivalente
        filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
        
        # Înlocuiește caracterele nepermise în numele de fișier
        filename = re.sub(r'[\\/:"*?<>|]', '', filename)

        return more_sanitization(filename)

    from lib_common import text_to_pdf, text_to_docx, replace_special_characters
    
    cdir = abspath(dirname(__file__))
    input_dir = join(cdir, 'input_pdfs')
    
    SPLIT_MARKER_FILE = join(input_dir, "__split")
    CACHE_FILE = join(input_dir, "__process_cache.txt")
    process_files_base = []
    if exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            for l in f.readline():
                if len(l.strip()) > 0:
                    process_files_base.append(l)
                    
    if exists(SPLIT_MARKER_FILE):        
        from lib_fuzzy_indexes_parser import find_filename_relevant_indexes
        from random import randint
        print("converting pdfs to docxs...")
        for filename in listdir(input_dir):
            if filename.endswith('.pdf'):
                pdf_file = join(input_dir, filename)
                docx_file = join(input_dir, filename[:filename.rfind(".")] + "docx")
                # convert pdf to docx
                print(f"{pdf_file}->{docx_file}")
                cv = Converter(pdf_file)
                cv.convert(docx_file, start=0, end=None)
                cv.close()
                remove(pdf_file)
                
        print("\nspliting docxs into sections...")
        for filename in listdir(input_dir):
            if filename.endswith('.doc') or filename.endswith('.docx'):
                process_files_base.append(filename)
        process_files_base = process_files_base[:3]
        process_files_base = list(map(lambda e: e[:e.rfind(".")], process_files_base))
        
        #import pdb; pdb.set_trace()
        for filename in listdir(input_dir):
            if filename.endswith('.doc') or filename.endswith('.docx'):
                doc_file = join(input_dir, filename)
                sections = _pp_combine_empty_titles(_pp_fix_sublists(_extract_sections(doc_file)))
                #import pdb; pdb.set_trace()
                try:
                    key_ = filename[:filename.rfind(".")]
                    process_files = process_files_base[:]
                    process_files.append(key_)
                    index = find_filename_relevant_indexes(process_files)[key_]
                except:
                    index = randint(1, 10000)
                sub_index = 1
                for title, text in sections.items():
                    #new_file = join(input_dir, sanitize_filename(f"{index}.{sub_index}-{title}.pdf"))
                    new_file = join(input_dir, sanitize_filename(f"{str(index).zfill(2)}.{str(sub_index).zfill(2)}-{title}.docx"))
                    print(f"{filename}:{new_file}")
                    #text_to_pdf(replace_special_characters(text), new_file)
                    text_to_docx(replace_special_characters(text), new_file)
                    sub_index += 1
                remove(doc_file)
    else:
        print("Nu exista fisierul __split.txt, deci lasam documentele intregi, asa cum sunt, pdf-uri sau doc-uri, caci pasul urmator va stii sa se descurce si cu unul si cu celalalt")