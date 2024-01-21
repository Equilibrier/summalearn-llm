from fuzzywuzzy import process
import re

# NU-mi mai trebuie nici asta si nici build_fixupper_lookup.py (desi logica e brilianta, ideea mea si implementarea chatgpt + a mea :D) deci mai poate fi folosita -- read_pdf si read_doc imi stricau, de fapt, textul cu lower() iar nu chatgpt

def build_lookup(reference_text):
    sentences = re.split('[.!?]', reference_text)
    words = []

    for sentence in sentences:
        split_sentence = sentence.strip().split()
        if len(split_sentence) > 1:
            words.extend([word for word in split_sentence[1:] if word.istitle() or word.isupper()])

    lookup = [(word.lower(), word.isupper()) for word in set(words)]

    return lookup

def correct_text(text_to_correct, lookup, threshold=90):
    words_to_correct = re.split('(\W+)', text_to_correct)

    for i, word in enumerate(words_to_correct):
        if word.isalnum():
            #if word.lower() == "o":
            #    import pdb; pdb.set_trace()
            if len(word) > 2:
                match = process.extractOne(word, [tup[0] for tup in lookup if len(tup[0]) > 2], score_cutoff=threshold)
                if match:
                    is_acronim = [tup[1] for tup in lookup if tup[0] == match[0]][0]
                    if is_acronim:
                        words_to_correct[i] = word.upper()
                    else:
                        words_to_correct[i] = word.capitalize()

    return "".join(words_to_correct)

if __name__ == "__main__":
    lookup = build_lookup("E bine in Bucuresti, caci este un oras frumos. Iar NATO este o organizatie internationala.")
    print(correct_text("bucuresti este un oras frumos. nato este o organizatie internationala.", lookup))
