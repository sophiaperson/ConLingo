# Sophia Ho
# language.py (15-112 Fall 2018 Term Project)
# AndrewID: swho
# Recitation: P

class Language(object):
    def __init__(self, sentenceStruct, syllableStruct, gender, negationPlace, 
        negationConj, tensePlace, tenseConj, adjPlace, pluralityPlace, 
        pluralityConj, accusePlace, accuseConj, nomPlace, nomConj, datePlace, 
        dataConj, genPlace, genConj, name):
        self.sentenceStruct = sentenceStruct
        self.syllableStruct = syllableStruct
        self.gender = gender
        self.negationPlace, self.negationConj = negationPlace, negationConj
        self.tensePlace, self.tenseConj = tensePlace, tenseConj
        self.adjPlace = adjPlace
        self.nomPlace, self.nomConj = nomPlace, nomConj
        self.pluralityPlace, self.pluralityConj = pluralityPlace, pluralityConj
        self.accusePlace, self.accuseConj = accusePlace, nomConj
        self.datePlace, self.dateConj = datePlace, dateConj
        self.genPlace, self.genConj = genPlace, genConj
        self.name = name
    def __repr__(self):
        return self.name