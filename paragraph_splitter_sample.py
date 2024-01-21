
import re

text2 = '''
Omul care va varsa sange si al lui va fi varsat, caci Dumnezeu a facut pe om dupa chipul Sau" (Gen. 9, 5-6). Dupa traditia iudaica, Legea Noahica (a lui Noe), ar fi continut cam urmatoarele sapte porunci (Sanhedrin 56, 1-2): 1. Sa nu traiesti fara capetenie; 2. Sa te abtii de la nelegiuiri; 3. Sa te abtii de la cultul idolatru. Dupa caderea in pacat, omul a ramas inclinat spre rau (Gen. 6, 5; 8, 2), in special spre placerile carnii (Gen. 8, 7; 9, 22). Omul insa trebuie sa-si stapaneasca pasiunile (Gen. 4, 7).

'''

text3 = '''
Nicaieri ca in Israel si deci si in timpul patriarhilor, Dumnezeu nu era luat ca martor in juramintele ce se faceau (Gen. 21, 23; 24, 3; 25, 33; 26, 28, 50, 25). Dumnezeu era implorat sa-si arate voia Sa printr-un semn.
'''

text4 = '''
Domnia glorioasa a primilor trei regi (Saul 1032-1012 i. Hr. Hr.,David 1012-972 i.Hr. si Solomon 973-933 i. Hr.), este urmata de decadenta spirituala, morala si sociala.
'''

text5 = '''
Legamantul poporului cu Yahweh, concretizat in raspunsul lor religios
fata de Lege si relatia teocratica instalata, dar respectata cu intermitenta,
au determinat evolutia istorica a Israelului. Chiar daca aspectele religioase
practice, prevazute de Lege, nu mai au valabilitate astazi, in ceea ce
priveste relatia cultica cu Dumnezeu, aspectele spirituale sunt aceleasi,
bazate pe credinta, sinceritate, curatia inimii si morala elementara. Carti
istorice sunt urmatoarele: Pentateuhul: - expune istoria creatiei, a primilor
oameni, a salvarii neamului omenesc prin Noe. Apoi expune istoria
poporului evreu prin patriarhii Avraam, Isaac si Iacov, evolutia lor istorica
in contextul salasluirii in Egipt timp de patru secole, exodul si peripetiile
pregrinarii prin Sinai pana la cucerirea Canaanului. Iosua Navi: - expune
istoria cuceririi Canaanului si impartirea lui teritoriala de catre cele
douasprezece triburi ale Israelului, ca urmare a implinirii promisiunilor
divine facute lui Avraam. Judecatori: - expune istoria trecerii de la o viata
nomada la cea sedentara, cu implicatiile si consecintele descentralizarii
politice si administrative, mai ales din perspectiva religioasa, ceea ce
atrage inevitabil sanctiuni si lectii din partea lui Yahweh. Perioada istorica
implicata se incadreaza, fara posibilitatea elucidarii, intre 50 si 200 de ani.
Ruth: - expune un episod semnificativ din istoria mantuirii universale, cu
implicatii asupra genealogiei Mantuitorului Hristos. I IV Regi: - expun
istoria regalitatii israelite de la instalarea acesteia, la jumatatea sec. XI
i.Hr. si pana la anul 586 i.Hr., anul distrugerii Ierusalimului si desfiintarii
regatului Iuda. Domnia glorioasa a primilor trei regi (Saul 1032-1012
i.Hr., David 1012-972 i.Hr. si Solomon 973-933 i.Hr.), este urmata de
decadenta spirituala, morala si sociala. Regatul unitar se imparte inegal,
fara posibilitate de reconciliere, in 933 i.Hr., cele doua regate rezultate
avand intre ele relatii alternante de amicitie, sau razboi. Regatul Israel
(Efraim, sau de Nord), va fi inghitit in 722 i.Hr. de catre imperiul asirian,
iar Regatul Iuda va disparea si el in 586 i.Hr., fiind cucerit de catre
babiloniei. O mare parte dintre evrei vor continua sa traiasca in exil. I II
Paralipomena (Cronici): - expun anumite evenimente considerate
semnificative, din perioada regilor Israelului, unele dintre ele omise in
cartile Regi. Ezdra si Neemia: - expun restaurarea religioasa, sociala si
nationala a evreilor intorsi din exil, incepand cu primul lot de repatriati din
538 i.Hr., cu toate problemele inerente acestei refaceri. Primul obiectiv
este reconstruirea templului si restaurarea Ierusalimului, cu toate
implicatiile sociale in contextul continuitatii lor nationale incadrata de
imperiul persan din care fac parte acum. Evenimentele relatate se intind
pana la jumatatea secolului V i.Hr. Estera: - expune un moment crucial in
istoria evreilor raspanditi in marele imperiu persan, ce ar fi condus la
extinctia lor, daca nu ar fi intervenit pronia divina. In acelasi timp, cartea
prezinta modus vivendis iudaicorum in diaspora, ca model al supravietuirii
lor intr-un context total diferit fata de pamantul Canaanului.
Anaghinoscomena istorice (Tobit, Iudita, III Ezdra, I-III Macabei, Istoria
Suzanei, Istoria idolului Bel si a balaurului): - expun fiecare, anumite
evenimente demne de apreciat sub imboldul religiozitatii si al
spiritualitatii degajate (omitand valoarea doctrinara), petrecute fie in
diaspora evreiasca, fie pe teritoriul Palestinei, in etapa istorica dintre sec.
VI i.Hr. si mergand pana in sec. II i.Hr.
'''

text6 = "sa afle: 1. O scurta biografie a lui Iisus Hristos, 2. Un rezumat al invataturii Sale mesianice, 3."

text7 = '''
Cea dintai Evanghelie care a vazut 18.299 lumina zilei (asa cum considera in mod traditional o mare parte a cercetatorilor), este cea alcatuita in limba aramaica de catre Sfantul Apostol Matei si tradusa apoi in limba greaca. Aceasta Evanghelie a fost scrisa mai ales pentru crestinii proveniti dintre iudei. Din aceasta cauza, autorul, Evanghelistul Matei, are o abordare specifica: 1. staruie asupra dovedirii mesianitatii Mantuitorului cu texte din Vechiul Testament, 2. acorda o atentie deosebita cuvintarilor rostite de Domnul inaintea poporului, 3. Dupa Sfantul Matei urmeaza, in ordine canonica Sfantul Marcu, autorul Evangheliei a doua. Scrierea sa este adresata indeosebi crestinilor recrutati dintre pagani. Din aceasta cauza, Sfantul Marcu staruie mai ales asupra faptelor si minunilor savarsite de Domnul, spre a demonstra cititorilor ca Iisus Hristos, Cel ce porunceste si naturii si oamenilor si demonilor, este cu adevarat Fiul lui Dumnezeu Celui Viu si singur adevarat si atotputernic. Cuprinsul Evangheliei dupa Sf. Marcu (16 capitole) se imparte in doua mari sectiuni aproape egale:  istorisirea activitatii Mantuitorului in Galileea (I9).  istorisirea activitatii in Iudeea si in Ierusalim (X16). Referatul asupra activitatii Domnului in Galileea este precedat, in chip firesc, de o scurta introducere (I, 113), in care Sf. Marcu arata ca Evanghelia lui Iisus Hristos, Fiul lui Dumnezeu, s-a inceput cu predica Sf. Ioan Botezatorul si apoi cu Botezul si intreita ispitire a Domnului, fapte care s-au petrecut in Iudeea. Referatul asupra activitatii Mantuitorului in Iudeea se incheie, in chip logic, cu istorisirea ultimei Sale aratari catre cei 11 apostoli si cu inaltarea Sa la cer, fapte care s-au petrecut in Galileea (16, 1420). In compunerea scrierii sale, Sf. Marcu urmeaza de aproape pe Sf. Matei, din care lasa la o parte mai ales cuvintarile Mantuitorului. Planul Evangheliei a doua este topologic. Spre deosebire de Sf. Matei, Sf. Marcu manifesta insa si unele preocupari cronologice. Scrierea sa cuprinde pretioase informatii despre portretul si activitatea lui Iisus Hristos ca om adevarat si ca Dumnezeu adevarat. Ea este astfel o opera istorica, catehetica si apologetica.
'''

text7 = "Apar in Evanghelia sa surprinzator de multe femei: Elisabeta; proorocita Ana; mama vaduva a tanarului din Nain; pacatoasa din casa lui Simon fariseul."

text 

def lookup_biblice():
    vechiul_testament = ["geneza", "facere", "exodul", "iesirea", "levitic", "numerii", "deuteronomul", "iosua", "judecatori", "rut", "regi1", "1regi", "regi2", "2regi", "regi3", "3regi", "regi4", "4regi", "cronici1", "paralelipomena1", "1paralelipomena", "cronici2", "paralelipomena2", "2paralelipomena", "ezdra", "neemia", "estera", "iov", "psalmi", "proverbe", "ecclesiastul", "cantarea cantarilor", "isaia", "ieremia", "plangerile ieremia", "iezechiel", "daniel", "osea", "amos", "miheia", "ioil", "avdie", "iona", "naum", "avacum", "sofonie", "agheu", "zaharia", "maleahi"] # ar mai fi de completat

    noul_testament = ["matei", "marcu", "luca", "ioan", "faptele apostolilor", "romani", "corinteni1", "1corinteni", "corinteni2", "2corinteni", "galateni", "efeseni", "filipeni", "coloseni", "tesaloniceni1", "tesaloniceni2", "timotei1", "1timotei", "timotei2", "2timotei", "tit", "filimon", "evrei", "iacov", "petru1", "1petru", "petru2", "2petru", "ioan1", "1ioan", "ioan2", "2ioan", "ioan3", "3ioan", "iuda", "apocalipsa"]
    
    def genereaza_combinatiile(lista):
        comb_lista = []
        vocale = set('aeiouAEIOU')  # setul de vocale
        for cuvant in lista:
            for i in range(2, min(len(cuvant), 5) + 1):  
                comb_lista.append(cuvant[:i])

            # cautam prima consoana dupa prima litera si o adaugam la lista
            for litera in cuvant[1:]:  # pornim de la a doua litera
                if litera not in vocale:
                    comb_lista.append(cuvant[0] + litera)
                    #break  # ne oprim dupa ce am gasit prima consoana -, nu, continuam ! fiindca la marcu, avem mc, unde c e a doua consoana, de exemplu

        return comb_lista

    return genereaza_combinatiile(vechiul_testament) + genereaza_combinatiile(noul_testament)

SHORTCUTS_LOOKUP = [
    "sec", "fer", "sf", "etc", "pt",
] + lookup_biblice() + [re.compile(r'[iIdD]+.*[hH]+[rR]*.*')]


def is_word_shortcut(text):

    for s in SHORTCUTS_LOOKUP:
        if type(s) == str:
            if s.lower() == text.lower():
                return True
                
        elif isinstance(s, re.Pattern):
            if s.search(text.lower()) is not None:
                return True
            
    return False

def between_two_numbers(text, delimitator_pos):
    # Ne asigurăm că pos nu este la începutul sau sfârșitul textului
    if delimitator_pos == 0 or delimitator_pos == len(text) - 1:
        return False

    # Obținem caracterul la poziția specificată
    char = text[delimitator_pos]

    # Divizăm textul în două părți
    before = text[:delimitator_pos+1]
    after = text[delimitator_pos:]

    # Construim regex-urile pentru a căuta grupuri de cifre înainte și după caracter
    regex_before = r'\d+\s*{}\s*$'.format(re.escape(char))
    regex_after = r'^\s*{}\s*\d+'.format(re.escape(char))

    # Verificăm dacă regex-urile se potrivesc cu părțile de text
    return re.search(regex_before, before) is not None and re.search(regex_after, after) is not None
    

def extract_words_before_char(text, char_pos, num_words=1, include_given_char = False):
    words = text[:char_pos + (1 if include_given_char else 0)].split()
    return ' '.join(words[-num_words:]) if len(words) >= num_words else ' '.join(words)
    
def extract_words_after_char(text, char_pos, num_words=1, include_given_char = False):
    words = text[char_pos + (0 if include_given_char else 1):].split()
    return ' '.join(words[:num_words]) if len(words) >= num_words else ' '.join(words)

def is_numbered_list_index(text):
    pattern = re.compile(r'\b(([0-9]+)|([ivxlcdmIVXLCDM]+))\.')
    return pattern.search(text) is not None
    

def is_number(text):
        def is_float(s):
            try:
                float(s)
                return True
            except ValueError:
                return False
        def is_integer(s):
            return s.isdigit()

        return is_float(text) or is_integer(text)

paragraphs = []
i = 0
start_p = 0
in_numbered_list = False
in_paranthesis_counter = 0 # daca presupun ca nu o sa fie paranteze imbricate (structuri recursive), atunci pot face doar un boolean cu False si True; daca vreau sa tin cont de imbricari, tin un contor, dar problema e daca cineva uita sa inchida o paranteza (suntem, totusi, intr-un text literal, nu cod de programare) - as putea sa tin cont de o lungime maxim a parantezei, si sa se "prescrie" inchiderea ei daca cumva s-a uitat, si probabil ca e bine sa fac asa, ca si in cazul celelalt ar trebui facuta asa ceva - de ce ? fiindca daca presupun ca o paranteza e deschisa, orice punct din interior nu va mai avea efect de paragraf, si mi se pare normal, dar e o regula exhaustiva, daunatoare daca nu e contextul corect)
in_paranthesis_positions = []
in_paranthesis_max_length = 400
def add_paragraph(to_p_inclusive):
    global paragraphs, start_p, i
    p = text[start_p:to_p_inclusive + 1].replace('\n', '').strip()
    if len(p) > 0:
        paragraphs.append(p)
        start_p = to_p_inclusive + 1
        return start_p + 1
    return i + 1
    
def try_parse_paranthesis(current_char, current_position):
    global in_paranthesis_counter, in_paranthesis_positions
    if current_char == "(":
        in_paranthesis_counter += 1
        in_paranthesis_positions.append(current_position)
    elif current_char == ")":
        if in_paranthesis_counter >= 1:
            in_paranthesis_counter -= 1
            in_paranthesis_positions.pop()
        else:
            in_paranthesis_counter = 0
            in_paranthesis_positions = []
            print(f"AVERTISMENT: Avem o paranteza inchisa ) la pozitia {current_position} ({text[current_position-10:current_position+10]}) care nu are corespondent de paranteza deschisa - a fost ignorata")
    else:
        if in_paranthesis_counter > 0 and current_position - in_paranthesis_positions[-1] >= in_paranthesis_max_length:
            in_paranthesis_counter -= 1
            in_paranthesis_positions.pop()
            print(f"AVERTISMENT: ultima paranteza deschisa nu a mai avut corespondent dupa {in_paranthesis_max_length} caractere. AM inchis-o fortat")
    
def acknowledge_i_position_change(new_i):
    if new_i < len(text):
        global i
        for p in range(i + 1, new_i):
            try_parse_paranthesis(text[p], p)
    else:
        print(f"AVERTISMENT: acknowledge_i_position_change: mi s-a dat o pozitie new_i care depaseste stringul initial: {new_i} (maximul e {len(text) - 1})")
    i = new_i
    
while i < len(text):
    # luam delimitatoarele pe rand, si la lucruri din astea, e neaparat nevoie sa tratezi lucrurile cu o claritate si simplitate deosebita, fiindca sunt (inca) lucruri sintactice, dar de profunzime, si sintaxa inseamna structura in adancime

    # ceva logica de stare
    try_parse_paranthesis(text[i], i)

    # A. ! sau ? sunt delimitatoare sigure -> incheiam paragraful
    if text[i] == '!' or text[i] == '?':
        next_word = extract_words_after_char(text, i, 1)
        if next_word not in "!?:.": # daca urmeaza un alt delimitator, il ignoram pe asta
            acknowledge_i_position_change(add_paragraph(i))
            continue
        
    # B. punctul e punct (de delimitare paragraf) daca urmeaza dupa el o fraza. Are doar doua exceptii:
    #       - 1- scurtatura:
    #           -1.1- sub-exceptie, scurtatura de carti biblice, nu intotdeauna exista un standard dar se poate genera o multime de sub-scurtaturi pentru fiecare sursa biblica in parte - imi trebuie un lookup sau un regex sau o functie de validare
    #           -1.2- expresii "de epoca", adica cele din categoria inainte/dupa Mantuitorul Hristos (idH,iH,dH,...) - tot un lookup e bun si aici, sau un regex...
    #       - 2- index la o lista numerotata: grup de cifre sau litere (mici sau mari sau intercalate-greseala-tipizare) romane urmate de punctul nostru de aici - lista se recunoaste cel mai bine prin pastrarea starii (adica a analizelor anterioare) tinand seama ca am inceput o lista cand am avut un ":" anterior, avem acum sau am mai avut si dupa acest delimitator, indecsi de lista (descrisi mai sus) si inca nu am iesit din lista numerotata (iesire fiind un punct de delimitare care nu e urmat de un index de lista numerotata)
    
    elif text[i] == '.':
        next_word = extract_words_after_char(text, i, 1)
        if next_word not in "!?:.": # daca urmeaza un alt delimitator, il ignoram pe asta
        
            if in_paranthesis_counter <= 0: # NUMAI daca NU suntem in interiorul unor paranteze
                
                if not is_word_shortcut(extract_words_before_char(text, i, 1)) and not between_two_numbers(text, i):
                    # mai poate fi cazul 1 sau cazul cu "1." de exemplu (lista) - trebuie sa delimitam:
                    last_word = extract_words_before_char(text, i, 1, include_given_char=True)
                    if in_numbered_list and is_numbered_list_index(last_word):
                        #import pdb; pdb.set_trace()
                        pos_before_list_number = text.rfind(last_word)
                        if pos_before_list_number > -1:
                            acknowledge_i_position_change(add_paragraph(pos_before_list_number - 1))
                            continue
                        else:
                            print(f"avertisment: pos_before_list_number ar trebui sa fie mai mare ca -1 pentru last_word '{last_word}'")
                    else:
                        if not(is_number(extract_words_before_char(text, i, 1).strip()) and not in_numbered_list): # cazul versetelor, de exemplu, nu sunt in lista (nu am avut : ) dar sunt cu . dupa un numar, care e verset biblic sau orice altceva
                            if not is_numbered_list_index(extract_words_after_char(text, i, 1)):
                                in_numbered_list = False
                            acknowledge_i_position_change(add_paragraph(i))
                            continue
        
    # C. ":" varianta de excludere standard ar fi aceea in care, ca la unele referentieri biblice nestandardizate, te pomenesti ca ai grup de cifre inainte si dupa acest semn
    #  si ca o optimizare, ideea ar fi sa nu inchei paragraful neaparat decat daca urmeaza o lista numerotata
    elif text[i] == ":":
        next_word = extract_words_after_char(text, i, 1)
        if next_word not in "!?:.": # daca urmeaza un alt delimitator, il ignoram pe asta

            if in_paranthesis_counter <= 0: # NUMAI daca NU suntem in interiorul unor paranteze
            
                if is_numbered_list_index(extract_words_after_char(text, i, 1)) and not between_two_numbers(text, i):
                    in_numbered_list = True
                    acknowledge_i_position_change(add_paragraph(i))
                    continue
        
    # D. la ; o idee e sa nu fiu intre doua paranteze ( si ) ca atunci e clar ca nu inchei fraza;
    # iarasi cazul de excludere ca delimitator dintre doua grupuri de cifre
    # iarasi, sa nu fie intre doua numere, ca uneori, de ex la versete biblice, apare si acest delimitator
    # pentru economie de spatiu, daca nu ma aflu intr-o lista numerotata, atunci nu mai adaug un alt paragraf, ci las sa curga aceasta sectiune cu ; in continuare 
    # PE SCURT: NUMAI in liste numerotate, aplicam sectionare pe ; pentru paragraf nou
    elif text[i] == ';':
        next_word = extract_words_after_char(text, i, 1)
        if next_word not in "!?:.": # daca urmeaza un alt delimitator, il ignoram pe asta
            if in_paranthesis_counter <= 0: # NUMAI daca NU suntem in interiorul unor paranteze            
                if not text[start_p:i].rfind("(") > text[start_p:i].rfind(")") and not between_two_numbers(text, i) and in_numbered_list:
                    acknowledge_i_position_change(add_paragraph(i))
                    continue
        
    i += 1 # pt cazurile in care nu s-a apelat add_paragraph si continue, incrementam pentru urmatorul caracter
    
if len(text[start_p:i].strip()) > 0:
    paragraphs.append(text[start_p:i].replace('\n', '').strip())
    

print(paragraphs)
print(len(paragraphs))


#pattern2 = re.compile(r':\s*([a-zA-Z0-9]+\.)+$')
pattern2 = re.compile(r':\s*([a-zA-Z0-9]+\.\s*.*)*[a-zA-Z0-9]+\.\s*$')
s = pattern2.search(text)
print(s)
print("DA" if s is not None else "NU")