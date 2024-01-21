import re
from typing import List
from itertools import groupby, combinations
from operator import itemgetter
from fuzzywuzzy import fuzz
from collections import Counter


def _extract_common_words_and_numbers(file_names):
    words_and_numbers = []
    
    # Extragem cuvintele si numerele
    
    def pre_process_filename(string): # elimina spatiile de la extremitatile stanga si dreapta ale numerelor, ca sa forteze ca nici un numar sa nu existe de unul singur (fiindca logica fuzzy nu o sa stie ca aia e, de fapt, similaritate 100%) -- nu e nici pe departe ideal, dar acopera unele cazuri, mai corect ar fi sa elimine doar spatii de stanga sau dreapta in functie de o formula care sa fie identica pentru toate numerele pozitionate "cam tot pe acolo" -- ideea e ca numerele sa nu fie nici singure, dar nici sa se sudeze de toate stringurile, ca de ex "abc 12 blahhh" si "abc 12 oricealtceva" nu va iesi bine
        pattern = r'\b\s+(\d+)|(\d+)\s+\b'
        transformed_string = re.sub(pattern, r'\1\2', string)
        return transformed_string

    def transform_digits_to_X(string):
        transformed_string = re.sub(r'\d', 'X', string)
        return transformed_string
    
    for file_name in file_names:
        transformed_filename = pre_process_filename(file_name)
        words_in_file = re.findall(r'\b\w+\b', transformed_filename)
        words_and_numbers.extend((transform_digits_to_X(word), word, file_name) for word in words_in_file)
    
    # Calculam frecventa fiecarui cuvant si numar
    #frequency_counter = Counter(words_and_numbers)
    
    # Sortam cuvintele si numerele dupa frecventa lor si le transformam in tupluri cu 3 elemente
    #common_words_and_numbers = [(key[0], value, key[1]) for key, value in sorted(frequency_counter.items(), key=lambda x: -x[1])]
    
    #return common_words_and_numbers
    return words_and_numbers


def _compute_combination_similarity(combination):
    # Implementați aici logica de calcul a scorului de similaritate pentru combinația dată
    # 'combination' este o listă de perechi de cuvinte (word, freq, file) în combinația curentă
    
    # Calculăm scorul de similaritate total și numărul de perechi de stringuri
    total_similarity = 0
    pair_count = 0
    for i in range(len(combination)):
        for j in range(i + 1, len(combination)):
            word1, original_word1, file1 = combination[i]
            word2, original_word2, file2 = combination[j]
            
            # Calculăm scorul de similaritate între word1 și word2 folosind fuzz.ratio()
            similarity = fuzz.ratio(word1, word2)
            
            # Adăugăm scorul de similaritate la scorul total
            total_similarity += similarity
            pair_count += 1
    
    # Calculăm scorul mediu de similaritate
    if pair_count > 0:
        average_similarity = total_similarity / pair_count
    else:
        average_similarity = 0
    
    return average_similarity


def _find_most_similar(file_names, count):
    common_words_and_numbers = _extract_common_words_and_numbers(file_names)
    
    scores = []
    combinations_limit = 500  # Limita de combinații dorită
    combination_count = 0
    for combination in combinations(common_words_and_numbers, count):
        #print("###: ", combination)
        #import pdb; pdb.set_trace()
        combination_scores = []
        for pair in combination:
            word, original_word, file = pair
            combination_scores.append((word, original_word, file))
        
        # Calculam scorul de similaritate pentru combinatia curenta
        total_score = _compute_combination_similarity(combination_scores)
        
        if total_score > 70:  # Ajustati acest numar dupa necesitatile dvs.
            scores.append((combination_scores, total_score))
            
        combination_count += 1
        if combination_count >= combinations_limit:
            print("Am atins deja numarul maxim de combinatii pentru ", file_names)
            break
    
    #import pdb; pdb.set_trace()
    # Sortam combinatiile de cuvinte dupa scor
    scores.sort(key=lambda x: -x[1])
    
    return scores

    
def _filter_tuples_with_numbers(tuples_list):
    filtered_tuples = []
    
    for tup in tuples_list:
        contains_number = True
        for item in tup[0]:
            if not any(char.isdigit() for char in item[1]):
                contains_number = False
                break
        if contains_number:
            filtered_tuples.append(tup)
    
    return filtered_tuples


def _extract_relevant_number(string, collision_index = -1): # -1 inseamna ultima potrivire de numere
    # Definim un pattern regex pentru a căuta un număr relevant
    pattern = r'\d+'  # Căutăm o secvență de cifre consecutive
    
    # Utilizăm funcția findall() din modulul re pentru a extrage toate potrivirile
    matches = re.findall(pattern, string)
    
    # Verificăm dacă există potriviri și returnăm numărul relevant
    if matches:
        return int(matches[collision_index])  # Extragem ultima potrivire ca număr relevant
    else:
        return None  # În caz contrar, returnăm None sau puteți ajusta comportamentul dorit
    
def find_filename_relevant_indexes(filenames):
    if len(filenames) <= 0:
        return {}
    if len(filenames) == 1:
        num = _extract_relevant_number(filenames[0], 0)
        result = {}
        result[filenames[0]] = num
        return result
        
    nuples = _filter_tuples_with_numbers(_find_most_similar(filenames, len(filenames)))
    max_nup = []
    max_score = 0.0
    for tup in nuples:
        if tup[1] > max_score:
            max_nup = tup[0]
            max_score = tup[1]
    final_result = {}
    for stup in max_nup:
        final_result[stup[2]] = _extract_relevant_number(stup[1])
    #print(final_result)
    return final_result

if __name__ == "__main__":
    print(find_filename_relevant_indexes(["curs04-bl12ahblah", "curs02-blahblahhhh", "curs13-h1hiih"]))
    