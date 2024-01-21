import re

def match_string_prefix(str1, str2):
    # Identificăm prefixul pentru primul string
    prefix1 = re.match(r'(-|\*|\+|\d+[\.\) ])', str1)
    prefix1 = prefix1.group() if prefix1 else None

    # Identificăm prefixul pentru al doilea string
    prefix2 = re.match(r'(-|\*|\+|\d+[\.\) ])', str2)
    prefix2 = prefix2.group() if prefix2 else None

    # Verificăm dacă ambele stringuri au prefixuri numerice
    if prefix1 and prefix2 and prefix1[:-1].isdigit() and prefix2[:-1].isdigit():
        return int(prefix1[:-1]) + 1 == int(prefix2[:-1])

    # Altfel, comparăm direct prefixurile
    return prefix1 == prefix2

# Testăm funcția
print(match_string_prefix("1. Titlu", "2. Alt titlu"))  # Ar trebui să afișeze True
print(match_string_prefix("1) Titlu", "2) Alt titlu"))  # Ar trebui să afișeze True
print(match_string_prefix("- Titlu", "- Alt titlu"))    # Ar trebui să afișeze True
print(match_string_prefix("* Titlu", "* Alt titlu"))    # Ar trebui să afișeze True
print(match_string_prefix("1. Titlu", "3. Alt titlu"))  # Ar trebui să afișeze False
print(match_string_prefix("1) Titlu", "- Alt titlu"))   # Ar trebui să afișeze False
print(match_string_prefix("- Titlu", "* Alt titlu"))    # Ar trebui să afișeze False
