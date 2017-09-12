import re
import string
import numpy as np
import pandas as pd
import os
import random
import xml.etree.ElementTree as ET



def get_n_words(text, number_of_words, name = None, report = False):
    '''Funktion to extract the first and last n words from a string
    long tells, if the file is too short to extract to distinct subsets of length number_of_words'''
    long = True
    
    words = text.split(' ')
    if len(words) < number_of_words*2:   # Double because I dont want that first and last have 'common' elements
        if report == True:
            print('WARNING: ' + name + ' has fewer than ' + str(number_of_words*2) + ' words! ' + str(len(words)))
        long = False
        
    # Die ersten N Wörter:
    first_words = words[:number_of_words]
    start = ' '.join(first_words)
    # Letzten N Wörter:
    last_words = words[-number_of_words:]
    end = ' '.join(last_words)
    return (start, end, long)
   


#### Test
# Kurze Test-Texte

#text1 = 'Sprengstoffexperten des und Landeskriminalamtes haben den Sprengsatz untersucht. Sie gehen davon aus, dass die Ladung aus den Inhaltsstoffen sogenannter Polenböller gebaut und offenbar per Funk gezündet wurde. Die Beamten stufen den Vorfall als besorgniserregend ein, da man eine derartige Sprengkraft bei vergleichbaren Fällen noch nicht gesehen habe. Eine Spezialeinheit der Polizei zur Aufklärung extremistisch orientierter Straftaten ermittelt. Neben der Spur nach Berlin geht sie auch der These nach, dass womöglich eine bisher unbekannte Gruppe in dem Haus, das zum Abriss vorgesehen ist, einen Sprengversuch unternommen hat.'
#text2 = 'Und das, obwohl die und Sache mit der Krim eigentlich klar ist Die russische Annexion der ukrainischen Halbinsel im Jahr 2014 war völkerrechtswidrig. Das sagt die Bundesregierung, das sagt die EU das sagt sogar die Linkspartei, schon 2014 festgehalten per Parteitagsbeschluss. Und trotzdem wollen manche Linke am liebsten nicht darüber sprechen.'
#text3 = 'US-Präsident Donald Trump schließt eine militärische Reaktion auf die Krise in Venezuela nicht aus. Es gebe mehrere Möglichkeiten, "darunter eine militärische Option, falls nötig", sagte Trump am Freitag in New Jersey. Konkrete Pläne für ein militärisches Eingreifen in Venezuela gibt es aber offenbar nicht. Ein Pentagon-Sprecher erklärte, zum jetzigen Zeitpunkt gebe es keine entsprechenden Anweisungen aus dem Weißen Haus.'
#text4 = 'Als am Freitagmorgen vergangener und Woche die Eilmeldungen zum überraschenden Fraktionswechsel der niedersächsischen Grünen-Abgeordneten Elke Twesten über die Nachrichtenagenturen liefen, wusste die Bundeskanzlerin längst Bescheid. Angela Merkel (CDU) hat einem Medienbericht zufolge vorab von der Wechsel der niedersächsischen Landtagsabgeordneten von den Grünen zur CDU erfahren. Das gehe aus einem Schreiben von Kanzleramtsstaatsminister Helge Braun an die Geschäftsführerin der SPD-Bundestagsfraktion, Christine Lambrecht hervor, berichteten die Zeitungen des Redaktionsnetzwerks Deutschland (RND). Demnach informierte der niedersächsische CDU-Landesvorsitzende Bernd Althusmann die Kanzlerin am Vortag des Wechsels telefonisch.'

#vector_with_text = [text1, text2, text3, text4]


#b1 = 'This is a 12385 sample'
#b2 = 'this is     ano>>ther $example!!!'
#vector_with_text = [b1, b2]



# Takes a path and opens all txt-files in that directory and returns a vector with the n first
# words, n last words from every text and a vector with the name of the authors, given that all
# files have the format author_title.txt
def open_text(path, number_of_words):
    vector_with_text = []
    vector_text_end = []
    authors = []
    for t in os.listdir(path):
        # Überspringe Dateien, die keine Txt sind:
        if t[-4:] != '.txt':
            continue
            
        aut = re.match(r'(\w*)_', t).group(1)
        authors.append(aut)
            
        name = path +'/'+ t
        file = open(name, 'r')   
        text = file.read()
        
        words = get_n_words(text, number_of_words, t)
        vector_with_text.append(words[0])
        vector_text_end.append(words[1])

    return vector_with_text, vector_text_end, authors
    

def open_xml(path, max_of_files = 5000, n_of_words = 500):
    ''' Takes a path and opens max_of_files xml files in that directory. From each file it extracts the
    n first and last words and gives the author-ID, if the filename is formatted as authorid.[...].xml
    remove specifies if '&' Symboles are deleted in the files'''
    text_start = []
    text_end = []
    author_id = []
    
    number_files = 0
    for f_name in os.listdir(path):
        # Just xml-Files:
        #if f_name[-4:] != '.xml':
        if not f_name.endswith('xml'):
            continue        
        
        if number_files >= max_of_files:
            break
                       
        file_path = path + '/' + f_name
        
        try:
            text = ''
            file = open(file_path, 'r')
            for line in file:
                if line.startswith('<'):
                    continue
                text += line.strip()
                
            start, end, long =  get_n_words(text, n_of_words, f_name, False)    # Gives start, end, long? (i.e. boolean if the file has fewer than n words)

            # If the document has to few words, skip this one
            if long == False:
                continue

            aut = re.match(r'(\d+).', f_name).group(1)
            author_id.append(aut)

            text_start.append(start)
            text_end.append(end)

            number_files += 1
            #print(f_name)
            
        except UnicodeDecodeError:
            #print('Encoding Error: ', f_name)
            pass
        except ValueError:
            print('Parse: file: ', f_name)
        
    return text_start, text_end, author_id





    
    
    
def old_open_xml(path, max_of_files = 5000, n_of_words = 500, remove = True):
    text_start = []
    text_end = []
    author_id = []
    
    number_files = 0
    for f_name in os.listdir(path):
        # Just xml-Files:
        #if f_name[-4:] != '.xml':
        if not f_name.endswith('xml'):
            continue        
        
        if number_files >= max_of_files:
            break
                       
        file = path + '/' + f_name
        
        # Remove &-Symbols (otherwise the xml Parser throws an error)
        if remove == True:
            f = open(file, 'r')
            text = f.read()
            f.close()
            text = text.translate({ord('&'): None})
            f_o = open(file, 'w')
            f_o.write(text)
            f_o.close()
                       
        with open(file, 'r') as xml_file:   # Umständlich damit UTF8 codierung -> Reicht nicht
            tree = ET.parse(xml_file)
#      tree = ET.parse(file)
        root = tree.getroot()
        
        text = ''
        for p in root.findall('post'): # Find all <post> entries
            text += p.text.strip()    # Build one long string without any newline characters and white spaces
        
        start, end, long =  get_n_words(text, n_of_words, f_name, False)    # Gives start, end, long? (i.e. boolean if the file has fewer than n words)
        
        # If the document has to few words, skip this one
        if long == False:
            continue
            
        aut = re.match(r'(\d+).', f_name).group(1)
        author_id.append(aut)
            
        text_start.append(start)
        text_end.append(end)
        
        number_files += 1
        
    return text_start, text_end, author_id



# Take a text and get all the n-grams with their freq as a dict

def get_freq(text, n = 4):
    '''Take a string and get all the n-grams with their freq as a dict'''
    text1 = text.lower()
#   text1 = re.sub(r'[.,-?!+"_()/$§%<>]', '', text1)   # Remove punctuation, RE slower than that:
    text1 = text1.translate({ord(char): None for char in string.punctuation + '0123456789'}) # Remove punctuation and digits
    text1 = re.sub(r'\s\s+',' ',text1)     # Remove double spaces
    words = text1.split(' ')
    
    grams = []
    # Identify all n-grams:
    for w in words:
        if len(w) < (n+1):
            grams.append(w.lower())
        else:
            for k in range(len(w)-n + 1):
                grams.append(w[k:k+n].lower())
                
    freq = {}
    for g in set(grams):
        c = grams.count(g)
        freq[g]= c
    return freq

def build_matrix(vector_with_text, k_highest_freq = 100000):
    ''' Take a array of texts and return a matrix (as a numpy array) with the tf-idf values for all n grams in the texts. Each row represents a text'''

# Matrix mit den Texten als Zeilen und den verschiedenen n-grams als Spalten. Die Einträge geben
# dann für jedes n-grams den tf-idf Wert in Bezug auf den Text an
    
    # WICHTIG:
    # total_text braucht für später die selbe Reihenfolge wie vector_with_text
    total_text = [get_freq(text) for text in vector_with_text] # Vector with all dictionaries of freq

    # Total_freq ist ein dict was für jedes in irgendeinem Text vorkommenden n-gram die Gesamt-
    # Vorkommenshäufigkeit speichert
    total_freq = {}
    for cfreq in total_text:
        for f in cfreq:
            if f in total_freq:
                total_freq[f] += cfreq[f]
            else:
                total_freq[f] = cfreq[f]  
    #print(total_freq)           
    #print(len(total_freq))
    
    
    # Get the n-grams with the k-hightest freq from all texts
    # If there are more n-grams than k_highest_freq, delate the least frequent ones
    if len(total_freq.keys()) > k_highest_freq:
        lowest_freq = sorted([x for x in total_freq.values()], reverse = True)[k_highest_freq]

        keys = total_freq.keys()
        for k in list(total_freq.keys()):
            if total_freq[k] < lowest_freq:    
                del total_freq[k]

        
    # Data_m als matrix, die für jedes n-gram die absolute Häufigkeit enthält
    data_m = np.empty((len(vector_with_text), len(total_freq.keys())))

    for t in enumerate(vector_with_text):
        freq_t = []                                     # Freq für alle n-grams für aktuellen Text, da vector erst um alle n-grams erweitert werden muss, die nicht in aktuellem Text sind
        for g in enumerate(total_freq.keys()):
            if g[1] in total_text[t[0]]:                # Wenn n-gram in aktuellem Text (toatl_text sollte die selbe Reihenfolge haben wir v_text)
                freq_t.append(total_text[t[0]][g[1]])   # Nehme aus vektor mit allen Freq, den Eintrag der zum Text entspricht und suche die Freq für das aktuelle n gram 
            else: 
                freq_t.append(0.0)
        data_m[t[0]] = freq_t                           # Neue Reihe in Dataframe mit dem index


    # Berechen Vektor mit der idf für jedes n-gram
    idf_m = np.log(data_m.shape[0] /np.array([(data_m[:,column]!= 0).sum() for column in range(data_m.shape[1])])) 

    # Berechne TF 
    data_m = data_m / np.sum(data_m, axis = 1)[:,None]
    
    # Berechne TF-IDF
    data_m = np.multiply(data_m, idf_m)
    
    #print(data_m)
    return data_m


def pair_vec(n):
    '''The index corresponds to the start index, the entry to the text in end
    A Pair is from the same author if index = entry. 
    ATTENTION: By chance it can happen, that slithly more than 50% are from the same other, but never less
    '''


    x = list(range(n))
    #random.seed(0)
    rand_ind = random.sample(range(n), round(n / 2))
    rand_match = rand_ind.copy()
    random.shuffle(rand_match)
    
    for ent in x:
        if ent in rand_ind:
            x[ent] = rand_match.pop()

    return x

