# Sophia Ho
# conLangCreator.py (15-112 Fall 2018 Term Project)
# AndrewID: swho
# Recitation: P

"""Program creates a constructed language based on user inputted criteria and
saves words in data file for use in a language learning game"""

########################################
# Language Creation Logic
########################################
import random
import os
import phonology
import phones
import morphology
import syntax

# function assigns legal vowels (vowel bank compiled from English, French, and 
# Spanish)
def assignLegalVowels():
    vowels = set()
    allVowels = list(phones.createVowels())
    numVowels = random.randint(5, 10)
    for i in range(numVowels):
        vowels.add(allVowels[i])
    return vowels

# function assigns legal consonants (consonant bank compiled from English, 
# French, Spanish, and German)
def assignLegalConsonants():
    consonants = set()
    allConsonants = list(phones.createConsonants())
    numConsonants = random.randint(15, 25)
    for i in range(numConsonants):
        consonants.add(allConsonants[i])
    return consonants

# function assigns legal syllable structure
def assignSyllableStructure(structure=[0, 0, 0]):
    if structure != [0, 0, 0]:
        return structure
    numConsonantsOnset = random.randint(0, 2)
    numVowelsNucleus = random.randint(1, 2)
    numConsonantsCoda = random.randint(0, 2)
    return (numConsonantsOnset, numVowelsNucleus, numConsonantsCoda)
    
### Global Variables (Legal Vowels, Legal Consonants, Syllable Structure) ###
legalVowels = assignLegalVowels()
legalConsonants = assignLegalConsonants()
syllableStructure = assignSyllableStructure()
    
# function compares phones using sonority hierarchy
def isSonorityHierarchy(phone1, phone2):
    for consonant in legalConsonants:
        print("phone1:", phone1, "consonant:", type(consonant), consonant)
        if phone1[-1] == str(consonant):
            sonority = consonant.sonority
        print(legalConsonants)
    return sonority >= phone2.sonority

# function returns true if onset is legal
def isLegalOnset(onset, consonant):
    return not isSonorityHierarchy(onset, consonant)

# function returns true if coda is legal
def isLegalCoda(coda, consonant):
    return isSonorityHierarchy(coda, consonant)

# function finds random legal consonant
def randomLegalConsonant():
    return random.sample(legalConsonants, 1)[0]

# function finds random legal vowel
def randomLegalVowel():
    return random.sample(legalVowels, 1)[0]

# function creates onset    
def createOnset(onsetStruct):
    onset = ""
    for i in range(onsetStruct):
        consonant = randomLegalConsonant()
        if len(onset) == 0 or (str(consonant) not in onset and 
            isLegalOnset(onset, consonant)):
            onset += str(consonant)
    return onset

# function creates nucleus
def createNucleus(nucleusStruct):
    nucleus = ""
    for i in range(nucleusStruct):
        vowel = randomLegalVowel()
        if len(str(vowel)) == 0 or str(vowel) not in nucleus:
            nucleus += str(vowel)
    return nucleus

# function creates coda    
def createCoda(codaStruct):
    coda = ""
    for i in range(codaStruct):
        consonant = randomLegalConsonant()
        if len(coda) == 0 or (str(consonant) not in coda and isLegalCoda(coda, 
            consonant)):
            coda += str(consonant)
    return coda

# function creates syllable based on phonetic rules
def createSyllable():
    onsetStruct, nucleusStruct, codaStruct = syllableStructure
    onset = createOnset(onsetStruct)
    nucleus = createNucleus(nucleusStruct)
    coda = createCoda(codaStruct)
    syllable = onset + nucleus + coda
    if len(syllable) > 0:
        return syllable
    else:
        return createSyllable()

# function assigns conjugation rules (verb tense, negation, case, determiners)
def assignTenseConjugation(place=-1, conj=[]):
    pass

def assignNounConjugation(ending=[], nominative=[], accusative=[], dative=[], 
    genitive=[], plurality=[]):
    pass

def assignAdjConjugation(ending=[], plurality=[]):
    pass

def assignVerbConjugation(ending=[], negationPlace=-1, negationConj=[], 
    casePlace=-1, caseConj=[]):
    pass
    
def assignDeterminers(nominative=[], accusitive=[], dative=[], genitive=[],
    plurality=[]):
    pass

# function assigns word to meaning in English
def createLexicon():
    lexicon = set()
    wordBank = readFile("wordBank.txt") # wordBank adapted from Swadesh 207 list
    
    for translation in wordBank.splitlines():
        engWord, partOfSpeech = translation.split("\t")
        word = ""
        numSyllables = random.randint(1, 2)
        for i in range(numSyllables): 
            word += createSyllable()
        if partOfSpeech == "noun": lexicon.add(morphology.Noun())
    return lexicon

# function assigns sentence structure (SVO, SOV, VOS, etc.)
def assignSentenceStructure():
    possibleStructures = ['svo', 'sov', 'vos', 'vso', 'osv', 'ovs']
    senStrucIndex = random.randint(0, len(possibleStructures) - 1)
    return possibleStructures[senStrucIndex]

# function adapted from 15-112 website course notes
def readFile(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

# function adapted from 15-112 website course notes
def writeFile(path, contents):
    with open(path, "wt", encoding="utf-8") as f:
        f.write(contents)

# function creates and stores language as series of rules and vocabulary in 
# folder of files
def createLanguage():
    vowels = str(legalVowels)[1:-1]
    consonants = str(legalConsonants)[1:-1]
    syllables = str(syllableStructure)[1:-1]
    lexicon = str(createLexicon())[1:-1]
    os.makedirs("./languages/testLanguage", exist_ok=True)
    writeFile("languages/testLanguage/legalVowels.txt", vowels)
    writeFile("languages/testLanguage/legalConsonants.txt", consonants)
    writeFile("languages/testLanguage/syllableStructure.txt", syllables)
    writeFile("languages/testLanguage/lexicon.txt", lexicon)
    sentenceStructure = assignSentenceStructure()