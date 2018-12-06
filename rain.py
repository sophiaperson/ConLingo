# Sophia Ho
# raining object class
# andrewID: swho
# Recitation: P

# adapted from hack112 KanjiRain Object
class RainingWord(object):
    def __init__(self, pronunciation, meaning, partOfSpeech, position, size,
        fallSpeed):
        self.pronunciation = pronunciation # meaning of word 
        self.meaning = meaning # the meaning in english
        self.posx = position[0] # x value of the current position
        self.posy = position[1] # y value of the current position
        self.size = size 
        self.defaultRainSpeed = 7
        self.partOfSpeech = partOfSpeech
        if fallSpeed != None:
            self.fallSpeed = fallSpeed
        else:
            self.fallSpeed = self.defaultRainSpeed 
    
    def calculateRainSpeed(self):
        lenWord = len(self.word)
        return self.defaultRainSpeed - lenWord
    
    def moveDown(self):
        self.posy += self.fallSpeed

    def isCollidingWithBottom(self, data):
        return (self.posy + 20 + self.size) > data.height

    def isCollidingWithSection(self, data):
        pass