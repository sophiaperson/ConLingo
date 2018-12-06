# Sophia Ho
# conLangGame2.py (15-112 Fall 2018 Term Project)
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
    if newWord[2] in {"noun", "verb,transitive", "verb,intransitive", "adjective", 
    "adverb"}:
        rightBound = int(data.width - len(newWord[1]) * data.wordSize)
        data.rainWord = (rain.RainingWord(
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
    else:
        addNewRainingWord(data)

def wordCollisions(data): # remove the word when it hits the bottom of screen
    if data.rainWord.isCollidingWithBottom(data):
        didScore = False
        sections = [[0, data.width/4, "noun"], 
        [data.width/4+1, data.width/2, "verb"], 
        [data.width/2+1, data.width*3/4, "adjective"], 
        [data.width*3/4+1, data.width, "adverb"]]
        for section in sections:
            x0, x1, name = section
            posx = (data.rainWord.posx + len(data.rainWord.pronunciation) * 
            data.rainWord.size / 2)
            if x0 <= posx <= x1 and name in data.rainWord.partOfSpeech:
                data.score2 += 1
                didScore = True
        if not didScore:
            data.lives2 -= 1
        data.rainWord = None

def moveWords(data):
    if data.rainWord != None:
        data.rainWord.moveDown()

def runEveryFrame(data): # run this every animation frame
    if data.rainWord == None:
        addNewRainingWord(data)
    moveWords(data)
    wordCollisions(data)

def drawWords(canvas, data):
    try: 
        canvas.create_text(
            data.rainWord.posx,
            data.rainWord.posy,
            anchor = "nw",
            text = data.rainWord.pronunciation,
            font = 'Arial ' + str(data.rainWord.size) + ' bold'
        )
    except:
        addNewRainingWord(data)

def drawSections(canvas, data):
    blockWidth = data.width / 4
    blockHeight = data.height  / 5
    margin = 30
    for i in range(4):
        if i == 0: 
            color, partOfSpeech = "pink", "noun"
        elif i == 1: 
            color, partOfSpeech = "yellow", "verb"
        elif i == 2: 
            color, partOfSpeech = "lightblue", "adjective"
        elif i == 3: 
            color, partOfSpeech = "lightgreen", "adverb"
        midX = (blockWidth * i + blockWidth * (i + 1)) / 2 
        midY = (data.height + (data.height - blockHeight)) / 2 - margin
        canvas.create_rectangle(blockWidth * i, data.height - blockHeight - margin, 
        blockWidth * (i + 1), data.height - margin, fill=color)
        canvas.create_text(midX, midY, text=partOfSpeech, font="Ariel "+
        str(int(data.width / 50)))
        

# --------------------------------------------------------- #
# -------------- Animation Functions ---------------------- #
# --------------------------------------------------------- #

def gameTimerFired(data):
    data.currGameTime += 1
    runEveryFrame(data)

def runGame(canvas, data):
    drawSections(canvas, data)
    drawWords(canvas, data)