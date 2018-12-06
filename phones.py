# Sophia Ho
# phones.py (15-112 Fall 2018 Term Project)
# AndrewID: swho
# Recitation: P

import phonology

### Phone Bank of All Possible Phones (Global Dictionaries) ###

allVowels = {'a':'unrounded tense low front', 'e':'unrounded tense mid front', 
            'i':'unrounded tense high front', 'o':'unrounded tense mid back', 
            'u':'rounded tense high back', 'ɪ':'unrounded lax high front', 
            'ʊ':'rounded lax high back', 
            'ə':'unrounded lax mid central','ɛ':'unrounded lax mid front', 
            'ɔ':'rounded lax mid back', 
            'æ':'unrounded lax low front', 'ɑ':'unrounded lax low back'}
        
allConsonants = {'m':'voiced bilabial nasal', 
    'n':'voiced alveolar nasal', 
    'ŋ':'voiced velar nasal', 'p':'unvoiced bilabial stop', 
    'b':'voiced bilabial stop', 't':'unvoiced alveolar stop', 
    'd':'voiced alveolar stop', 'k':'unvoiced velar stop', 
    'ɡ':'voiced velar stop','s':'unvoiced alveolar fricative', 
    'z':'voiced alveolar fricative', 'ʃ':'unvoiced post-Alveolar fricative', 
    'ʒ':'voiced post-Alveolar fricative', 'ɸ':'unvoiced bilabial fricative', 
    'β':'voiced bilabial fricative', 'f':'unvoiced labiodental fricative',	
    'v':'voiced labiodental fricative', 'θ':'unvoiced interdental fricative', 
    'ð':'voiced interdental fricative', 'x':'unvoiced velar fricative', 
    'ɣ':'voiced velar fricative', 'h':'unvoiced glottal fricative',
    'ɹ':'voiced alveolar retroflex liquid', 'j':'voiced palatal glide', 
    'l':'voiced alveolar lateral liquid',
    'w':'voiced bilabial glide'}

allPhones = allVowels.copy()
allPhones.update(allConsonants)

def createVowels():
    vowelObjects = set()
    for vow in allVowels:
        roundedness, tenseness, height, advancement = allVowels[vow].split(" ")
        vowelObjects.add(phonology.Vowel(vow, tenseness, height, roundedness,
        advancement))
    return vowelObjects
    
def createConsonants():
    consonantObjects = set()
    for consonant in allConsonants:
        attributes = allConsonants[consonant].split(" ")
        voicing, place = attributes[0], attributes[1]
        if len(attributes) == 3: manner = attributes[2]
        else: manner = attributes[2] + " " + attributes[3]
        consonantObjects.add(phonology.Consonant(consonant, voicing, place, 
        manner))
    return consonantObjects