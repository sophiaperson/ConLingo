# Sophia Ho
# conLangGame.py (15-112 Fall 2018 Term Project)
# andrewID: swho
# Recitation: P

######################################
# Language Learning Game Logic
######################################

# Adapted from hack112 wordRain game

from tkinter import *
import rain
import os
import random

# function adapted from 15-112 website course notes
def readFile(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

# function adapted from 15-112 website course notes
def writeFile(path, contents):
    with open(path, "wt", encoding="utf-8") as f:
        f.write(contents)

# function adds new word to set of raining words 
def addNewRainingWord(data):
    newWord = data.wordBank[random.randint(0, len(data.wordBank) - 1)]
    newWord = newWord.split("\t")
    rightBound = int(data.width - len(newWord[1]) * data.wordSize)
    data.rainingWords.add(rain.RainingWord(
        pronunciation = newWord[1],
        meaning = newWord[0],
        partOfSpeech = newWord[2],
        position = (
            random.randint(0, rightBound),
            0
        ),
        size = data.wordSize,
        fallSpeed = 3
    ))

def wordCollisions(data): # remove the word when it hits the bottom of screen
    wordsToRemove = set()
    for word in data.rainingWords:
        if word.isCollidingWithBottom(data):
            wordsToRemove.add(word)
            data.lives1 -= 1
    for word in wordsToRemove:
        data.rainingWords.remove(word)

def runEveryFrame(data): # run this every animation frame
    moveWords(data)
    wordCollisions(data)

def runEveryWordAddInterval(data):# run this every second
    addNewRainingWord(data)

def moveWords(data):
    for word in data.rainingWords:
        word.moveDown()

def drawWords(canvas, data):
    for word in data.rainingWords:
        assert(type(word) == rain.RainingWord)
        canvas.create_text(
            word.posx,
            word.posy,
            anchor = "nw",
            text = word.pronunciation,
            font = 'Arial ' + str(word.size) + ' bold'
        )

def checkAnswer(data):
    currentAnswer = data.input
    wordsToRemove = set()
    for word in data.rainingWords:
        if currentAnswer == word.pronunciation:
            # remove the word from falling list
            wordsToRemove.add(word)
            data.score1 += 1
    for word in wordsToRemove:
        data.rainingWords.remove(word)


# --------------------------------------------------------- #
# -------------- Animation Functions ---------------------- #
# --------------------------------------------------------- #

def gameTimerFired(data):
    data.currGameTime += 1
    runEveryFrame(data)
    if data.currGameTime % data.wordFreqency == 0:
        runEveryWordAddInterval(data)

def runGame(canvas, data):
    drawWords(canvas, data)