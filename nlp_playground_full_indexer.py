import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text

from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter, Filter, StandardAnalyzer
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from nltk.stem.snowball import SnowballStemmer
import os

class DiacriticsFilter(Filter):
    replacements = {
        '\u0103': 'a', '\u0102': 'a',  # ă
        '\u00E2': 'a', '\u00C2': 'a',  # â
        '\u00EE': 'i', '\u00CE': 'i',  # î
        '\u0219': 's', '\u0218': 's',  # ș
        '\u021B': 't', '\u021A': 't',  # ț
        '\u015F': 's', '\u015E': 's',  # ș cu cedilla
        '\u0163': 't', '\u0162': 't'   # ț cu cedilla
    }

    def __call__(self, tokens):
        for t in tokens:
            for diacritic, replacement in self.replacements.items():
                t.text = t.text.replace(diacritic, replacement)
            yield t


class RomanianStemFilter(Filter):
    def __init__(self):
        self.stemmer = SnowballStemmer("romanian")

    def __call__(self, tokens):
        for t in tokens:
            t.text = self.stemmer.stem(t.text).replace("ind", "")  # Elimină gerunziul
            yield t

def create_searchable_data(schema, indexdir, text):
    if not os.path.exists(indexdir):
        os.mkdir(indexdir)
    ix = create_in(indexdir, schema)
    writer = ix.writer()
    writer.add_document(content=text)
    writer.commit()

def search_query(indexdir, query_str):
    ix = open_dir(indexdir)
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)
        for result in results:
            print(result.highlights("content"))

def stop_words_ro():
	'''
Articole: un, o, niste, unele, unii, unei, unor

Pronume personale: eu, tu, el, ea, noi, voi, ei, ele, mine, tine, sine, noi, voi, lor

Pronume posesive: meu, mea, mei, mele, tau, ta, tai, tale, sau, sa, sai, sale, nostru, noastra, nostri, noastre, vostru, voastra, vostri, voastre

Pronume reflexive: ma, te, se, ne, va

Pronume demonstrative: acesta, aceasta, acestea, aceia, acela, aceea, acele, acei

Prepoziții: la, de, din, cu, pe, pentru, intre, spre, prin, peste, fara, dupa, contra, printre, fara, langa, despre, sub, pana, prin

Conjuncții: si, dar, daca, cand, pentru ca, desi, ori, sau, decat, asadar, prin urmare, totusi, fie

Interjecții: ah, oh, ei, bah
'''
	return set(['a', 'abia', 'acea', 'aceasta', 'aceasta', 'aceea', 'aceeasi', 'acei', 'aceia', 'acel', 'acela', 'acelasi', 'acele', 'acelea', 'acest', 'acesta', 'aceste', 'acestea', 'acestei', 'acestia', 'acestui', 'acesti', 'acestia', 'acolo', 'acord', 'acum', 'adica', 'ai', 'aia', 'aiba', 'aici', 'aiurea', 'al', 'ala', 'alaturi', 'ale', 'alea', 'alt', 'alta', 'altceva', 'altcineva', 'alte', 'altfel', 'alti', 'altii', 'altul', 'am', 'anume', 'apoi', 'ar', 'are', 'as', 'asa', 'asemenea', 'asta', 'astazi', 'astea', 'astfel', 'astazi', 'asupra', 'atare', 'atat', 'atata', 'atatea', 'atatia', 'ati', 'atit', 'atita', 'atitea', 'atitia', 'atunci', 'au', 'avea', 'avem', 'aveti', 'avut', 'azi', 'as', 'asadar', 'ati', 'b', 'ba', 'bine', 'bucur', 'buna', 'c', 'ca', 'cam', 'cand', 'capat', 'care', 'careia', 'carora', 'caruia', 'cat', 'catre', 'caut', 'ce', 'cea', 'ceea', 'cei', 'ceilalti', 'cel', 'cele', 'celor', 'ceva', 'chiar', 'ci', 'cinci', 'cind', 'cine', 'cineva', 'cit', 'cita', 'cite', 'citeva', 'citi', 'citiva', 'conform', 'contra', 'cu', 'cui', 'cum', 'cumva', 'curand', 'curind', 'cand', 'cat', 'cate', 'catva', 'cati', 'cind', 'cit', 'cite', 'citva', 'citi', 'ca', 'caci', 'carei', 'caror', 'carui', 'catre', 'd', 'da', 'daca', 'daca', 'dar', 'dat', 'datorita', 'data', 'dau', 'de', 'deasupra', 'deci', 'decit', 'degraba', 'deja', 'deoarece', 'departe', 'desi', 'despre', 'desi', 'din', 'dinaintea', 'dintr', 'dintr-', 'dintre', 'doar', 'doi', 'doilea', 'doua', 'drept', 'dupa', 'dupa', 'da', 'e', 'ea', 'ei', 'el', 'ele', 'era', 'eram', 'este', 'eu', 'exact', 'esti', 'f', 'face', 'fara', 'fata', 'fel', 'fi', 'fie', 'fiecare', 'fii', 'fim', 'fiu', 'fiti', 'foarte', 'fost', 'frumos', 'fara', 'g', 'geaba', 'gratie', 'h', 'halba', 'i', 'ia', 'iar', 'ieri', 'ii', 'il', 'imi', 'in', 'inainte', 'inapoi', 'inca', 'incit', 'insa', 'intr', 'intre', 'isi', 'iti', 'j', 'k', 'l', 'la', 'le', 'li', 'lor', 'lui', 'langa', 'linga', 'm', 'ma', 'mai', 'mare', 'mea', 'mei', 'mele', 'mereu', 'meu', 'mi', 'mie', 'mine', 'mod', 'mult', 'multa', 'multe', 'multi', 'multa', 'multi', 'multumesc', 'maine', 'miine', 'ma', 'n', 'ne', 'nevoie', 'ni', 'nici', 'niciodata', 'nicaieri', 'nimeni', 'nimeri', 'nimic', 'niste', 'niste', 'noastre', 'noastra', 'noi', 'noroc', 'nostri', 'nostru', 'nou', 'noua', 'noua', 'nostri', 'nu', 'numai', 'o', 'opt', 'or', 'ori', 'oricare', 'orice', 'oricine', 'oricum', 'oricand', 'oricat', 'oricind', 'oricit', 'oriunde', 'p', 'pai', 'parca', 'patra', 'patru', 'patrulea', 'pe', 'pentru', 'peste', 'pic', 'pina', 'plus', 'poate', 'pot', 'prea', 'prima', 'primul', 'prin', 'printr-', 'putini', 'putin', 'putina', 'putina', 'pana', 'pina', 'r', 'rog', 's', 'sa', 'sa-mi', 'sa-ti', 'sai', 'sale', 'sau', 'se', 'si', 'sint', 'sintem', 'spate', 'spre', 'sub', 'sunt', 'suntem', 'sunteti', 'sus', 'suta', 'sint', 'sintem', 'sinteti', 'sa', 'sai', 'sau', 't', 'ta', 'tale', 'te', 'ti', 'timp', 'tine', 'toata', 'toate', 'toata', 'tocmai', 'tot', 'toti', 'totul', 'totusi', 'totusi', 'toti', 'trei', 'treia', 'treilea', 'tu', 'tuturor', 'tai', 'tau', 'u', 'ul', 'ului', 'un', 'una', 'unde', 'undeva', 'unei', 'uneia', 'unele', 'uneori', 'unii', 'unor', 'unora', 'unu', 'unui', 'unuia', 'unul', 'v', 'va', 'vi', 'voastre', 'voastra', 'voi', 'vom', 'vor', 'vostru', 'voua', 'vostri', 'vreme', 'vreo', 'vreun', 'va', 'x', 'z', 'zece', 'zero', 'zi', 'zice', 'ii', 'il', 'imi', 'impotriva', 'in', 'inainte', 'inaintea', 'incotro', 'incat', 'incit', 'intre', 'intrucat', 'intrucit', 'iti', 'ala', 'alea', 'asta', 'astea', 'astia', 'sapte', 'sase', 'si', 'stiu', 'ti', 'tie'])

# Parametrii și apelul funcțiilor
pdf_path = r".\pagini_extrase.pdf"
indexdir = "indexdir"
query_str = "atanasie crimca"
language = "ro"  # sau "en"

# Schema de indexare
if language == "ro":
    analyzer = RegexTokenizer() | LowercaseFilter() | DiacriticsFilter() | RomanianStemFilter() | StopFilter(stoplist=stop_words_ro())
else:
    analyzer = StandardAnalyzer()

schema = Schema(content=TEXT(analyzer=analyzer, stored=True))

# Procesarea PDF-ului
text = extract_text_from_pdf(pdf_path)

# Crearea indexului și căutarea
create_searchable_data(schema, indexdir, text)
search_query(indexdir, query_str)
