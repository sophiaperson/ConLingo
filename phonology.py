# Sophia Ho
# Phone Class
# andrewID: swho
# Recitation: P

class Phone(object):
    def __init__(self, symbol, voicing):
        self.symbol = symbol
        self.voicing = voicing
    def getHashables(self):
        return (self.symbol, self.voicing)
    def __hash__(self):
        return hash(self.getHashables())
    def __eq__(self, other):
        return (isinstance(other, Phone) and self.symbol == other.symbol and 
                self.voicing == other.voicing)

class Consonant(Phone):
    def __init__(self, symbol, voicing, place, manner):
        super().__init__(symbol, voicing)
        self.place = place
        self.manner = manner
        if self.manner == "glide": self.sonority = 4
        elif "liquid" in self.manner: self.sonority = 3
        elif self.manner == "nasal": self.sonority = 2
        elif self.manner == "fricative" or self.manner == "affricate": 
            self.sonority = 1
        elif self.manner == "stop": self.sonority = 0
    def __repr__(self):
        return (self.symbol)

class Vowel(Phone):
    def __init__(self, symbol, tenseness, height, roundedness, advancement,
        voicing="voiced"):
        super().__init__(symbol, voicing)
        self.height = height
        self.roundedness = roundedness
        self.sonority = 5
        self.tenseness = tenseness
        self.advancement = advancement
    def __repr__(self):
        return (self.symbol)