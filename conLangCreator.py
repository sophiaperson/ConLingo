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
def assignSylStruct(structure=[0, 0, 0]):
    if structure != [0, 0, 0]:
        return structure
    numConsonantsOnset = random.randint(0, 2)
    numVowelsNucleus = 1
    numConsonantsCoda = random.randint(0, 2)
    result = (numConsonantsOnset, numVowelsNucleus, numConsonantsCoda)
    if result != (0, 1, 0): return result
    else: return(assignSylStruct())


### Global Variables (Legal Vowels, Legal Consonants, Syllable Structure) ###
legalVowels = assignLegalVowels()
legalConsonants = assignLegalConsonants()
    
# function compares phones using sonority hierarchy
def isSonorityHierarchy(phone1, phone2):
    for consonant in legalConsonants:
        if phone1[-1] == str(consonant):
            sonority = consonant.sonority
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
def createSyllable(sylStruct):
    onsetStruct, nucleusStruct, codaStruct = sylStruct
    onset = createOnset(onsetStruct)
    nucleus = createNucleus(nucleusStruct)
    coda = createCoda(codaStruct)
    syllable = onset + nucleus + coda
    if len(syllable) > 0:
        return syllable
    else:
        return createSyllable(sylStruct)

# function assigns verb tense conjugation rules
def assignTenseConjugation(sylStruct, numTenseConj, place=-1):
    conj = []
    if place == -1: place = random.randint(0, 1) 
    # 0 -> tense conjugated at start of word,
    # 1 -> tense is conjugated at end
    if numTenseConj == -1: numTenseConj = random.randint(2, 3)
    # 2 -> language will not distinguish between present and future tense
    # 3 -> language will distinguish between present tense and future tense
    for i in range(numTenseConj): 
        conj += [createSyllable(sylStruct)]
    return (place, conj) # returns int and list

# function assigns negation rules
def assignNegationRule(sylStruct, place=-1):
    if place == -1: place = random.randint(0, 1)
    # 0 -> negation conjugated at start of word
    # 1 -> negation conjugated at end of word
    conj = createSyllable(sylStruct)
    return (place, conj) # returns int and str

# function assigns how and where different noun and adj conjugations are formed 
# in order of their application
def assignNounConjugation(sylStruct, numGender, isNomConj, isAccuseConj,
    isDativeConj, isGenitiveConj, isPlurConj=-1, place=-2):
    gender, nominative, accusative, dative = [], [], [], []
    print("yo", isNomConj, 
    isAccuseConj, isDativeConj, isGenitiveConj, isPlurConj)
    genitive, plurality = [], []
    # placement of conjugation
    place = random.randint(0, 1)
    if place != -1:
        for i in range(numGender): gender += [createSyllable(sylStruct)]
    if (isNomConj == -1 and isAccuseConj == -1 and isDativeConj == -1 and
    isGenitiveConj == -1):
        isNomConj = random.randint(0, 1)
        isAccuseConj = random.randint(0, 1)
        isDativeConj = random.randint(0, 1)
        isGenitiveConj = random.randint(0, 1)
    else: 
        if isNomConj == -1: isNomConj = 0
        elif isAccuseConj == -1: isAccuseConj = 0
        elif isDativeConj == -1: isDativeConj = 0
        elif isGenitiveConj == -1: isGenitiveConj = 0
    for i in range(isNomConj): nominative += [createSyllable(sylStruct)]
    for i in range(isAccuseConj): accusative += [createSyllable(sylStruct)]
    for i in range(isDativeConj): dative += [createSyllable(sylStruct)]
    for i in range(isGenitiveConj): genitive += [createSyllable(sylStruct)]
    if isPlurConj == -1: isPlurConj = random.randint(0, 1)
    for i in range(isPlurConj): plurality += [createSyllable(sylStruct)]
    return (place, gender, nominative, accusative, dative, genitive, plurality) 
    # returns int and lists

# function assigns generic adjective ending
def assignAdjAdvConjugation(sylStruct, numGender, place=-2):
    adjEnd, advEnd = [], ""
    if place==-2:
        place = random.randint(0, 1)
    for i in range(numGender):
        adjEnd += [createSyllable(sylStruct)]
    advEnd = createSyllable(sylStruct)
    return (place, adjEnd, advEnd) # returns int, list, and str
    
# function assigns which determiners exist    
def assignDeterminers(sylStruct, numGender, indefinite=-1, definite=-1):
    indefDet, defDet, pronouns = [], [], []
    if indefinite==-1 and definite==-1:
        indefinite = random.choice([True, False])
        definite = random.choice([True, False])
    else: 
        if indefinite == -1: indefinite = 0
        if definite == -1: definite = 0
    if indefinite: 
        for i in range(numGender): 
            indefDet += [createSyllable(sylStruct)]
    if definite:
        for i in range(numGender):
            defDet += [createSyllable(sylStruct)]
    for i in range(3):
        pronouns.append(createSyllable(sylStruct))
    return (indefDet, defDet, pronouns) # returns list and list

# function assings spelling of word based on its IPA reading
def assignWordSpelling(pronunciation):
    spelling = ""
    for c in pronunciation:
        for phone in phones.allPhones.keys():
            value = phones.allPhones[phone]
            if ("low front" in value or "low back" in value or "mid central"
            in value): 
                spelling += "a"
            elif "mid front" in value: spelling += "e"
            elif "high front" in value: spelling += "i"
            elif "high back" in value: spelling += "u"
            elif "mid back" in value: spelling += "o"
    return spelling # returns str

# function assigns word to meaning in English
# input: (int, list), (int, str), (int, lists), (int, str, str), (list, list)
def createLexicon(sylStruct, numGender, tenseConj, negationConj, nounConj,
    adjAdvConj, determiners):
    lexicon = dict()
    wordBank = readFile("wordBank.txt") # wordBank adapted from Swadesh 207 list
    for translation in wordBank.splitlines():
        engWord, partOfSpeech = translation.split("\t")
        word = createSyllable(sylStruct)
        # add noun / pronoun marking (gender)
        if "noun" in partOfSpeech and nounConj[0] != -1: # place of nounConj
            genderInt = random.randint(0, numGender - 1)
            if nounConj[0] == 0: word = nounConj[1][genderInt] + word
            word += nounConj[1][genderInt]
        # add verb marking (non-past is default tense)
        if "verb" in partOfSpeech: 
            if tenseConj[0] == 0: word = tenseConj[1][0] + word
            word += tenseConj[1][0]
        # add adj marking
        if partOfSpeech == "adjective":
            if adjAdvConj[0] == 0: word = adjAdvConj[1][0] + word
            word += adjAdvConj[1][0]
        # add adv marking
        if partOfSpeech == "adverb":
            if adjAdvConj[0] == 0: word = adjAdvConj[2] + word
            word += adjAdvConj[2]
        lexicon[engWord] = [word, partOfSpeech]
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
def createLanguage(syllables=[0,0,0], gender=-1, tenseConj=-1, negationConj=[],
    nounConj=[], adjAdvConj=[], indefinite=-1, definite=-1, sentenceStructure=""):
    # legal vowels and consonants are always randomized
    vowels = str(legalVowels)[1:-1]
    consonants = str(legalConsonants)[1:-1]
    # syllableStruct, tenseConj, negationConj, nounConj, adjAdvConj, 
    # and determiners can be user inputted
    sylStruct = assignSylStruct(syllables)
    syllables = str(sylStruct)[1:-1]
    if gender == -1: gender = random.randint(1, 3)
    tenseConj = assignTenseConjugation(sylStruct, tenseConj)
    negationConj = assignNegationRule(sylStruct)
    nom, accus, dat, gen = nounConj
    nounConj = assignNounConjugation(sylStruct, gender, nom, accus, dat, gen)
    adjAdvConj = assignAdjAdvConjugation(sylStruct, gender)
    determiners = assignDeterminers(sylStruct, gender, indefinite, definite)
    if sentenceStructure == "": sentenceStructure = assignSentenceStructure()
    # create vocabulary of language
    lexicon = createLexicon(sylStruct, gender, tenseConj, negationConj, nounConj,
    adjAdvConj, determiners)
    langName = lexicon["lang"][0]
    # save language
    saveLanguage(gender, vowels, consonants, syllables, lexicon, tenseConj,
    negationConj, nounConj, adjAdvConj, determiners, sentenceStructure, langName)
    return langName
    
# function saves language as series of rules and vocabulary in directory
def saveLanguage(numGender, vowels, consonants, syllables, lexicon, tenseConj,
    negationConj, nounConj, adjAdvConj, determiners, sentenceStructure, langName):
    dirName = "./languages/" + langName
    os.makedirs(dirName, exist_ok=True)
    vowelFilePath = "languages/" + langName + "/legalVowels.txt"
    consonantFilePath = "languages/" + langName + "/legalConsonants.txt"
    syllableFilePath = "languages/" + langName + "/syllableStructure.txt"
    sentStructFilePath = "languages/" + langName + "/sentenceStructure.txt"
    writeFile(vowelFilePath, vowels)
    writeFile(consonantFilePath, consonants)
    writeFile(syllableFilePath, syllables)
    writeFile(sentStructFilePath, sentenceStructure)
    saveTenseConj(tenseConj, langName)
    saveNegationConj(negationConj, langName)
    saveNounConj(nounConj, langName)
    saveAdjAdvConj(adjAdvConj, langName)
    saveDeterminers(determiners, langName)
    saveLexicon(lexicon, langName)

# function saves and formats tense conjugation rules
def saveTenseConj(tenseConj, langName):
    result = str(tenseConj[0]) + "\n" + str(tenseConj[1])
    tenseFilePath = "languages/" + langName + "/tenseConjugation.txt"
    writeFile(tenseFilePath, result)

# function saves and formats negation conjugation rules
def saveNegationConj(negationConj, langName):
    result = str(negationConj[0]) + "\n" + str(negationConj[1])
    negationFilePath = "languages/" + langName + "/negationConjugation.txt"
    writeFile(negationFilePath, result[:-1])
    
# function saves and formats noun conjugation rules
def saveNounConj(nounConj, langName):
    result = ""
    for i in range(len(nounConj)):
        result = result + str(nounConj[i]) + "\n"
    nounFilePath = "languages/" + langName + "/nounConjugation.txt"
    writeFile(nounFilePath, result[:-1])
    
# function saves and formats adj and adv conjugation rules
def saveAdjAdvConj(adjAdvConj, langName):
    result = ""
    for i in range(len(adjAdvConj)):
        result = result + str(adjAdvConj[i]) + "\n"
    adjAdvFilePath = "languages/" + langName + "/adjAdvConjugation.txt"
    writeFile(adjAdvFilePath, result[:-1])

# function saves and formats determiners
def saveDeterminers(determiners, langName):
    result = ""
    for i in range(len(determiners)):
        result = result + str(determiners[i]) + "\n"
    determinerFilePath = "languages/" + langName + "/determiners.txt"
    writeFile(determinerFilePath, result[:-1])

# function saves and formats lexicon
def saveLexicon(lexicon, langName):
    result = ""
    for key in lexicon:
        result = result + key + "\t"
        for i in range(2):
            result += str(lexicon[key][i]) + "\t"
        result += "\n"
    lexiconFilePath = "languages/" + langName + "/lexicon.txt"
    writeFile(lexiconFilePath, result[:-1])