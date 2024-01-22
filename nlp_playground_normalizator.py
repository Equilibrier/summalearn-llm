def normalize_romanian(text):
    # Conversia la lowercase
    text = text.lower()

    # Înlocuirea diacriticelor
    replacements = {
        '\u0103': 'a', '\u0102': 'a',  # ă
        '\u00E2': 'a', '\u00C2': 'a',  # â
        '\u00EE': 'i', '\u00CE': 'i',  # î
        '\u0219': 's', '\u0218': 's',  # ș
        '\u021B': 't', '\u021A': 't',  # ț
        '\u015F': 's', '\u015E': 's',  # ș cu cedilla
        '\u0163': 't', '\u0162': 't'   # ț cu cedilla
    }

    for diacritic, replacement in replacements.items():
        text = text.replace(diacritic, replacement)

    return text

# Testarea funcției
original_text = "Exemplu cu diacritice: Șarpe, Înghețată, Mărțișor, Țap"
normalized_text = normalize_romanian(original_text)
print(normalized_text)
