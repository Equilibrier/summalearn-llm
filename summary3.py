
import openai
import textwrap
import re
from time import sleep

from lib_common import read_pdf, read_docx

from transformers import GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

def segment_text_by_sentence(text, max_length):
    #import pdb; pdb.set_trace()
    sentences = re.split('(?<=[.!?]) +', text)
    segments = []
    current_segment = ""
    for sentence in sentences:
        if len(tokenizer.encode(current_segment + sentence + ".")) >= max_length:
            segments.append(current_segment)
            current_segment = sentence + "."
        else:
            current_segment += sentence + "."

    segments.append(current_segment)

    return segments

openai.api_key = "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"


def summarize_text_segment(segment):
    output = ""
    trials = 0
    error = True
    while trials < 5:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[ 
                    {"role": "user", "content": f"Rezuma-mi, in romaneste, următorul text, mai concis: {segment}"},
                    #{"role": "user", "content": f"Reformuleaza, in romaneste, următorul text: {segment}"},
                    #{"role": "user", "content": f"Reformuleaza, in romaneste, următorul text, dar un pic mai concentrat: {segment}"},
                    #{"role": "user", "content": f"Reformuleaza, in romaneste, următorul text; redu din complexitate, dar pastreaza detaliile cele mai relevante. Iata textul sursa: {segment}"},
                ],
                temperature=0.05
            )
            output = response["choices"][0]["message"]["content"]
            error = False
            break
        except:
            trials += 1
            sleep(11)
    if error:
        print(f"Eroare: motorul chatgpt nu a putut fi instantiat (nici dupa 5 incercari) pentru textul: {segment}.\nRezumatul a fost resetat la ''")
            
    return output

def summarize_iteratively(text, max_length):
    # split text into segments based on max length
    segments = segment_text_by_sentence(text, max_length)
    summary_text = ""

    for segment in segments:
        new_summary_text = summarize_text_segment(segment)
        summary_text += new_summary_text + " "

    return summary_text

def summarize_one_file(in_file, out_file_txt):
    max_length = 1365 # text un intreg, raspuns o jumatate, rezulta 3 treimi, si textul initial 2 treimi, adica 4096 / 3 = 

    #target_length = 450  # Aiming for a summary of 600 tokens
    if in_file.lower().endswith(".pdf"):
        file_as_text = read_pdf(in_file)
    else:
        file_as_text = read_docx(in_file)
    
    #import pdb; pdb.set_trace()

    summary = file_as_text  # Initialize the summary as the full text
    token_count = len(tokenizer.encode(summary))
    
    target_length = max(token_count/3, 500)
    target_length = min(target_length, 1000)
    
    print(f"Cautam sa targetam un rezumat la {target_length} tokeni")
    
    processed_at_least_once = False
    steps = 0
    print(f"Iteratie curenta: {token_count} tokeni")
    
    while token_count > target_length or processed_at_least_once is False:  # Check the token count
        previous_summary = summary
        previous_token_count = token_count
        summary = summarize_iteratively(summary, max_length)
        token_count = len(tokenizer.encode(summary))
        if token_count == previous_token_count:
            print(f"ChatGPT nu mai rezuma mai mult, lasam lucrurile la valoarea de {token_count} tokeni")
            break
        print(f"Iteratie curenta: {token_count} tokeni")
        processed_at_least_once = True
        steps += 1
        
    if token_count < 500:
        summary = previous_summary
        print(f"revenim la varianta precedenta, ca sa fie peste valoarea minima de 500: {previous_token_count}...")
        steps -= 1

    print(f"Rezumat in {steps} pasi.")
    
    with open(out_file_txt, "w+", encoding="utf-8") as file:
        file.write(summary)

if __name__ == "__main__":
    from os.path import dirname, basename, join, isfile, splitext, exists
    from os import listdir, makedirs
    
    input_dir = "./input_pdfs"
    output_dir = "./output_txts"

    # creează directorul output_txts dacă nu există deja
    makedirs(output_dir, exist_ok=True)

    # parcurge fișierele din director
    for file in listdir(input_dir):
        # verifică dacă fișierul are extensia .pdf
        if file.lower().endswith(".pdf") or file.lower().endswith(".doc") or file.lower().endswith(".docx"):
            # construiește căile complete de intrare și ieșire
            input_file = join(input_dir, file)
            output_txt = join(output_dir, splitext(basename(file))[0] + ".txt")
            if not exists(output_txt):
                print(f"Nu am gasit (deja computat) fisierul {output_txt} asa ca il procesam prin chatGPT...")
                summarize_one_file(input_file, output_txt)
            else:
                print(f"Ignoram procesare pentru {input_file}. Fisierul txt deja a fost procesat, il consideram un cache si ignoram. Daca doriti sa fie regenerat, trebuie sa repuneti fisierul input in directorul de input si sa stergeti fisierul de output ({output_txt}) inainte de a da drumul la proces")
            
