from nltk.stem.snowball import SnowballStemmer

# Crearea stemmer-ului pentru limba română
stemmer = SnowballStemmer("romanian")

# Cuvinte de test
words = ["cărți", "carte", "citind", "cititor", "bibliotecă"]

# Aplică stemmer-ul pentru fiecare cuvânt
for word in words:
    stemmed = stemmer.stem(word)
    print(f"Original: {word}, Stemmed: {stemmed}")
