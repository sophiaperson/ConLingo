# Sophia Ho
# main.py (15-112 Fall 2018 Term Project)
# andrewID: swho
# Recitation: P

# Updated Animation Starter Code taken from 15-112 website

from tkinter import *
import display
import os
import phones
import conLangCreator
import conLangGame
import conLangGame2
import copy

####################################
# Display user interface 
####################################

# initializes data class attributes
def init(data):
    data.mode = "welcomeScreen"
    data.prevModes = ["welcomeScreen"]
    data.buttons = []
    data.prevButtons = []
    # store all user inputted language information here
    data.sentenceStructure = ""
    data.phones = set()
    data.syllables = [0, 0, 0]
    data.gender = -1
    data.tenseConj = []
    data.negationConj = []
    data.nounConj = [-1, -1, -1, -1]
    data.adjAdvConj = []
    data.determiners = []
    data.indefinite = -1
    data.definite = -1
    data.tenses = ""
    data.tenseNum = -1
    data.cases = []
    data.langName = ""
    # game1 data
    data.lives1 = 10
    data.timerCalls = 0
    data.rainingWords = set()
    data.score1 = 0
    data.currGameTime = 0
    data.wordFreqency = 25
    data.wordBank = []
    data.wordSize = int(data.width / 20)
    data.input = ""
    # game2 data
    data.lives2 = 10
    data.rainWord = None
    data.score2 = 0
    
# function that handles mouse click actions for user input phonology
def phonologyButtonAction(data, x, y):
    for i in range(len(data.buttons)):
        if (data.buttons[i].x0 <= x <= data.buttons[i].x1 and 
            data.buttons[i].y0 <= y <= data.buttons[i].y1):
            if data.buttons[i].name != "back":
                data.buttons[i].click()
                data.syllables[int(i/3)] = int(data.buttons[i].name)
            else:
                data.prevModes += [data.buttons[i].name]
                data.prevModes.pop()
                data.mode = data.prevModes[-2]
                data.prevModes.pop()

# function that handles mouse click actions for user input morphology
# gender (int), determiners(list of 2 ints)
def morphologyButtonAction(data, x, y):
    for i in range(len(data.buttons)):
        if (data.buttons[i].x0 <= x <= data.buttons[i].x1 and 
            data.buttons[i].y0 <= y <= data.buttons[i].y1):
            if data.buttons[i].name in {"1", "2", "3"}:
                data.buttons[i].click()
                data.gender = int(data.buttons[i].name)
            elif data.buttons[i].name in {"indefinite", "definite"}:
                data.buttons[i].click()
                if data.buttons[i].name not in data.determiners:
                    data.determiners.append(data.buttons[i].name)
                    if data.buttons[i].name == "indefinite": data.indefinite=1
                    else: data.definite=1
                elif data.buttons[i].name in data.determiners:
                    data.determiners.remove(data.buttons[i].name)
                    if data.buttons[i].name == "indefinite": data.indefinite=0
                    else: data.definite=0
            else:
                data.prevModes += [data.buttons[i].name]
                data.prevModes.pop()
                data.mode = data.prevModes[-2]
                data.prevModes.pop()

# checks sentence structure
def checkCaseAction(data, buttonName):
    if buttonName in data.cases:
        data.cases.remove(buttonName)
        if buttonName == "nominative": data.nounConj[0]=0
        elif buttonName == "accusative": data.nounConj[1]=0
        elif buttonName == "dative": data.nounConj[2]=0
        elif buttonName == "genitive": data.nounConj[3]=0
    else:
        data.cases.append(data.buttons[i].name)
        if buttonName == "nominative": data.nounConj[0]=1
        elif buttonName == "accusative": data.nounConj[1]=1
        elif buttonName == "dative": data.nounConj[2]=1
        elif buttonName == "genitive": data.nounConj[3]=1

# function that handles mouse click actions for user input syntax
# sentenceStructure (str), tenses (list), cases (list)
def syntaxButtonAction(data, x, y):
    for i in range(len(data.buttons)):
        if (data.buttons[i].x0 <= x <= data.buttons[i].x1 and 
            data.buttons[i].y0 <= y <= data.buttons[i].y1):
            if data.buttons[i].name in {'svo', 'sov', 'vos', 'vso', 'osv', 'ovs'}:
                data.sentenceStructure = data.buttons[i].name
            elif (data.buttons[i].name in 
            {"past / non-past", "past / present / future"}):
                data.tenses = data.buttons[i].name
                if data.tenses == "past / non-past":
                    data.tenseNum = 2
                elif data.tenses == "past / present / future":
                    data.tenseNum = 3
            elif (data.buttons[i].name in 
            {"nominative", "accusative", "dative", "genitive"}):
                checkCaseAction(data, data.buttons[i].name)
            else:
                data.prevModes += [data.buttons[i].name]
                data.prevModes.pop()
                data.mode = data.prevModes[-2]
                data.prevModes.pop()
                
# function handles mouse click actions for learnAllMenu
def learnButtonAction(data, x, y):
    for button in data.buttons:
        if (button.x0 <= x <= button.x1 and 
            button.y0 <= y <= button.y1):
            if button.name != "back":
                data.prevModes.append(button.name)
                data.langName = button.name
                data.mode = data.langName
            else: # implement action for clicking on back button
                data.prevModes.pop()
                data.mode = data.prevModes[-1]
                
# function handles mouse click actions for gameMenu
def gameMenuButtonAction(data, x, y):
    for button in data.buttons:
        if (button.x0 <= x <= button.x1 and 
            button.y0 <= y <= button.y1):
            print(button.name)
            if button.name != "back":
                data.prevModes.append("gameScreen")
                data.langName = button.name
                data.mode = "gameScreen"
                setWordBank(data)
            else: # implement action for clicking on back button
                data.prevModes.pop()
                data.mode = data.prevModes[-1]
     
# function sets wordBank
def setWordBank(data):
    lexiconPath = "languages/" + data.langName + "/lexicon.txt"
    data.wordBank = readFile(lexiconPath).splitlines()

# function does action if button is clicked
def mousePressed(event, data):
    if data.mode == "phonology" and data.prevModes[-2] == "custom":
        phonologyButtonAction(data, event.x, event.y)
    elif data.mode == "morphology" and data.prevModes[-2] == "custom":
        morphologyButtonAction(data, event.x, event.y)
    elif data.mode == "syntax" and data.prevModes[-2] == "custom":
        syntaxButtonAction(data, event.x, event.y)
    elif data.mode == "learn":
        learnButtonAction(data, event.x, event.y)
    elif data.mode == "game":
        gameMenuButtonAction(data, event.x, event.y)
    else:
        for button in data.buttons:
            if (button.x0 <= event.x <= button.x1 and 
                button.y0 <= event.y <= button.y1):
                data.prevModes += [button.name]
                if button.name == "done" or button.name == "random":
                    assignLanguageRules(data)
                if button.name != "back":
                    data.mode = button.name
                else: # implement action for clicking on back button
                    data.prevModes.pop()
                    data.mode = data.prevModes[-2]
                    data.prevModes.pop()
    
def keyPressed(event, data):
    if data.mode == "game1":
        if event.char.isalpha():
            data.input += event.char
        if event.keysym == "Return":
            conLangGame.checkAnswer(data)
            data.input = ""
        elif event.keysym == "BackSpace":
            if data.input != "": data.input = data.input[:-1]
    if data.mode == "game2" and data.rainWord != None:
        speed = 20
        wordBound = len(data.rainWord.pronunciation) * (data.wordSize) 
        if event.keysym == "Left" and data.rainWord.posx - 20 >= -wordBound:
            data.rainWord.posx -= speed
        elif (event.keysym == "Right" and data.rainWord.posx + 20 <= data.width):
            data.rainWord.posx += speed

# function checks if game is over
def gameOver1(data):
    if data.lives1 < 0:
        init(data)
        
# function checks if game is over
def gameOver2(data):
    if data.lives2 < 0:
        init(data)

def timerFired(data):
    if data.mode == "game1":
        conLangGame.gameTimerFired(data)
        if data.currGameTime % 2 == 0:
            gameOver1(data)
    if data.mode == "game2":
        conLangGame2.gameTimerFired(data)
        if data.currGameTime % 2 == 0:
            gameOver2(data)

# draws back button
def backButton(canvas, data):
    bottomMargin = data.height / 50
    sideMargin = data.width / 3
    buttonHeight = int(data.height / 10)
    labelSize = int(min(data.width, data.height) / 25)
    data.buttons += [display.Button("back", sideMargin, 
    data.height - bottomMargin - buttonHeight, data.width - sideMargin,
    data.height - bottomMargin, labelSize)]

### Creation Menu ###

# menu gives user the option of customizing their language or having its rules
# randomly generated
def drawCreateMenu(canvas, data):
    buttonNames = ["back", "custom", "random"]
    data.buttons = []
    sideMargin = data.width / 5
    bottomMargin = data.height / 20
    buttonHeight = data.height / 10
    buttonWidth = (data.width - sideMargin * 2) / len(buttonNames)
    labelSize = int(min(data.width, data.height) / 25)
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin,
        labelSize))
    canvas.create_text(data.width / 2, data.height / 5, 
    text="Let's create", font = "Ariel " + 
    str(int(data.height / 10)))
    canvas.create_text(data.width / 2, data.height * 2 / 5, 
    text="a new language!", font = "Ariel " + 
    str(int(data.height / 10)))

# menu allows user to customize certain aspects of the language
def drawUserCreateMenu(canvas, data):
    canvas.create_text(data.width / 2, data.height / 10, text="Choose settings",
    font = "Ariel " + str(int(data.height / 10)))
    canvas.create_text(data.width / 2, data.height / 5, 
    text="(unspecified variables will be randomized)")
    buttonNames = ["back", "phonology", "morphology", "syntax"]
    data.buttons = []
    sideMargin = data.width / 20
    bottomMargin = data.height / 20
    buttonHeight = data.height / 10
    buttonWidth = (data.width - sideMargin * 2) / len(buttonNames)
    labelSize = int(min(data.width, data.height) / 25)
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin,
        labelSize))
    data.buttons.append(display.Button("done", data.width / 2 - buttonWidth / 2, 
    data.height / 2 - buttonHeight / 2, data.width / 2 + buttonWidth / 2, 
    data.height / 2 + buttonHeight / 2, labelSize))

# create buttons for syllable structure
def syllableStructureButtons(canvas, data):
    buttonSize = data.width / 25
    topMargin = data.height / 5
    labelSize = int(data.width / 25)
    spacing = (data.width - (buttonSize * 9)) / 4
    sideMargin = spacing
    for i in range(3):
        for j in range(3):
            data.buttons.append(display.Button(str(j), sideMargin + 
            buttonSize * (j - 1), topMargin, sideMargin + buttonSize * j, 
            topMargin + buttonSize, labelSize))
        sideMargin = spacing + sideMargin + buttonSize * 3
        
# display user inputed syllable structure
def displaySyllableStructure(canvas, data):
    c1, v, c2 = data.syllables
    canvas.create_text(10, data.height / 3, anchor="nw", 
    text=str(c1), font = "Ariel " + 
    str(int(data.height / 50)))
    canvas.create_text(data.width / 2, data.height / 3, anchor="n", 
    text=str(v), font = "Ariel " + 
    str(int(data.height / 50)))
    canvas.create_text(data.width - 10, data.height / 3, anchor="ne", 
    text=str(c2), font = "Ariel " + 
    str(int(data.height / 50)))

# menu allows user to select syllable structure, legal consonants and vowels
def drawUserPhonologyMenu(canvas, data):
    data.buttons = []
    canvas.create_text(data.width / 2, data.height / 10, 
    text="Syllable Structure", font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(10, data.height / 7, anchor="nw", 
    text="Number of consonants in onset", font = "Ariel " + 
    str(int(data.height / 50)))
    canvas.create_text(data.width / 2, data.height / 7, anchor="n", 
    text="Number of vowels in nucleus", font = "Ariel " + 
    str(int(data.height / 50)))
    canvas.create_text(data.width - 10, data.height / 7, anchor="ne", 
    text="Number of consonants in coda", font = "Ariel " + 
    str(int(data.height / 50)))
    syllableStructureButtons(canvas, data)
    displaySyllableStructure(canvas, data)
    backButton(canvas, data)
    
# create buttons for morphology menu
def genderDeterminerButtons(canvas, data):
    buttonSizeGen = data.width / 25
    topMarginGen = data.height / 5
    labelSizeGen = int(data.width / 25)
    sideMarginGen = (data.width - buttonSizeGen * 3) / 2
    detLabels = ["indefinite", "definite"]
    for i in range(1, 4):
        data.buttons.append(display.Button(str(i), sideMarginGen + 
        buttonSizeGen * (i - 1), topMarginGen, sideMarginGen + buttonSizeGen * i, 
        topMarginGen + buttonSizeGen, labelSizeGen))
    buttonWDet = data.width / 5
    labelSizeDet = int(labelSizeGen * 0.75)
    buttonHDet = labelSizeDet + 5
    topMarginDet = data.height * 3 / 5
    sideMarginDet = (data.width - buttonWDet * 2) / 2
    for i in range(2):
        data.buttons.append(display.Button(detLabels[i], sideMarginDet + 
        buttonWDet * i, topMarginDet, sideMarginDet + buttonWDet * (i + 1), 
        topMarginDet + buttonHDet, labelSizeDet))
    
# displays selected gender number and determiners
def displayGenderDeterminer(canvas, data):
    buttonSizeGen = data.width / 25
    topMarginGen = data.height / 5
    labelSizeGen = int(data.height / 40)
    sideMarginGen = (data.width - buttonSizeGen * 3) / 2
    detLabels = ["indefinite", "definite"]
    canvas.create_text(data.width / 2, data.height / 10 + labelSizeGen * 2, 
    text="selected: " + str(data.gender), font="Ariel " + str(labelSizeGen))
    canvas.create_text(data.width / 2, data.height / 2 + labelSizeGen * 2,
    text="selected: " + str(data.determiners)[1:-1], font="Ariel " +
    str(labelSizeGen))
    
# menu allows user to select whether nouns have grammatical gender, 
# which pronouns exist (with some restrictions), and which determiners exist
def drawUserMorphologyMenu(canvas, data):
    data.buttons = []
    canvas.create_text(data.width / 2, data.height / 10, text="Gender", 
    font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 2, data.height / 2, text="Determiners",
    font = "Ariel " + str(int(data.height / 20)))
    genderDeterminerButtons(canvas, data)
    displayGenderDeterminer(canvas, data)
    backButton(canvas, data)

# creates buttons for user input syntax menu
def syntaxMenuButtons(canvas, data):
    sentStructButtons(canvas, data)
    tenseButtons(canvas, data)
    caseButtons(canvas, data)
    
# creates buttons for user input sentence structure
def sentStructButtons(canvas, data):
    sentStructs = ['svo', 'sov', 'vos', 'vso', 'osv', 'ovs']
    numStructs = len(sentStructs)
    buttonWidth = data.width / 10
    topMargin = data.height / 5
    labelSize = int(data.width / 25)
    buttonHeight = labelSize + 5
    sideMargin = (data.width - buttonWidth * numStructs) / 2
    for i in range(numStructs):
        data.buttons.append(display.Button(sentStructs[i], 
        sideMargin + buttonWidth * i, topMargin, sideMargin + buttonWidth * (i + 1),
        topMargin + buttonHeight, labelSize))

# creates buttons for user input tense
def tenseButtons(canvas, data):
    tenses = ["past / non-past", "past / present / future"]
    titleSize = int(data.height / 20)
    numStructs = len(tenses)
    buttonWidth = data.width / 3
    topMargin = data.height / 3 + titleSize * 2
    labelSize = int(data.width / 50)
    buttonHeight = labelSize + 5
    sideMargin = (data.width - buttonWidth * numStructs) / 2
    for i in range(numStructs):
        data.buttons.append(display.Button(tenses[i], 
        sideMargin + buttonWidth * i, topMargin, sideMargin + buttonWidth * (i + 1),
        topMargin + buttonHeight, labelSize))

# creates buttons for user input case
def caseButtons(canvas, data):
    cases = ["nominative", "accusative", "dative", "genitive"]
    titleSize = int(data.height / 20)
    numStructs = len(cases)
    buttonWidth = data.width / 5
    topMargin = data.height * 2 / 3 + titleSize * 2
    labelSize = int(data.width / 50)
    buttonHeight = labelSize + 5
    sideMargin = (data.width - buttonWidth * numStructs) / 2
    for i in range(numStructs):
        data.buttons.append(display.Button(cases[i], 
        sideMargin + buttonWidth * i, topMargin, sideMargin + buttonWidth * (i + 1),
        topMargin + buttonHeight, labelSize))
    
# displays buttons selected sentence structure, tenses, cases
def displaySyntax(canvas, data):
    titleSize = int(data.height / 20)
    fontSize = int(titleSize / 2)
    canvas.create_text(data.width / 2, data.height / 10 + titleSize, text=
    "selected: " + data.sentenceStructure, font="Ariel " + str(fontSize))
    canvas.create_text(data.width / 2, data.height / 3 + titleSize, text=
    "selected: " + data.tenses, font="Ariel " + str(fontSize))
    canvas.create_text(data.width / 2, data.height * 2 / 3 + titleSize, text=
    "selected: " + str(data.cases)[1:-1], font = "Ariel " + str(fontSize))

# menu allows user to select sentence structure, which tenses exist, and which
# cases exist
def drawUserSyntaxMenu(canvas, data):
    data.buttons = []
    canvas.create_text(data.width / 2, data.height / 10,
    text="Sentence Structure", font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 2, data.height / 3, text="Tenses",
    font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 2, data.height * 2 / 3, text="Cases",
    font = "Ariel " + str(int(data.height / 20)))
    syntaxMenuButtons(canvas, data)
    displaySyntax(canvas, data)
    backButton(canvas, data)

# assigns language rules and creates new language
def assignLanguageRules(data):
    data.langName = conLangCreator.createLanguage(data.syllables, data.gender,
    data.tenseNum, data.negationConj, data.nounConj, data.adjAdvConj,
    data.indefinite, data.definite, data.sentenceStructure)

# menu indicates that new language has been created
def drawComputerCreateMenu(canvas, data):
    buttonNames = ["back", "learn"]
    data.buttons = []
    sideMargin = data.width / 5
    bottomMargin = data.height / 20
    buttonHeight = data.height / 10
    buttonWidth = (data.width - sideMargin * 2) / len(buttonNames)
    labelSize = int(min(data.width, data.height) / 25)
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin,
        labelSize))
    canvas.create_text(data.width / 2, data.height / 5, text="Congrats!", 
    font = "Ariel " + str(int(data.height / 10)))
    canvas.create_text(data.width / 2, data.height * 2 / 5, 
    text="Your new language is " + data.langName + "!", font = "Ariel " + 
    str(int(data.height / 20)))

### Learning Menu ###

# function adapted from 15-112 website course notes
def readFile(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

# function adapted from 15-112 website course notes
def writeFile(path, contents):
    with open(path, "wt", encoding="utf-8") as f:
        f.write(contents)

# menu displays all saved languages    
def drawLearnAllMenu(canvas, data):
    canvas.create_text(data.width / 2, data.height / 10, text="Choose language", 
    font = "Ariel " + str(int(data.height / 10)))
    numLanguages = len(os.listdir("languages"))
    data.buttons = []
    sideMargin = data.width / 10
    topMargin = data.height / 5
    bottomMargin = data.height / 10
    labelSize = int(min(data.width, data.height) / 25)
    buttonHeight = data.height / 25
    backButtonHeight = data.height / 10
    smallLabelSize = int(buttonHeight)
    backSideMargin = data.width / 3
    for i in range(numLanguages):
        data.buttons += [display.Button(os.listdir("languages")[i], sideMargin, 
        topMargin + buttonHeight * i, data.width - sideMargin, 
        topMargin + buttonHeight * (i + 1), smallLabelSize)]
    backButton(canvas, data)

# menu displays language rules        
def drawLearnLangMenu(canvas, data):
    canvas.create_text(data.width / 2, data.height / 10, text=data.mode, 
    font = "Ariel " + str(int(data.height / 10)))
    buttonNames = ["back", "phonology", "morphology", "syntax"]
    data.buttons = []
    sideMargin = data.width / 20
    bottomMargin = data.height / 20
    buttonHeight = data.height / 10
    buttonWidth = (data.width - sideMargin * 2) / len(buttonNames)
    labelSize = int(min(data.width, data.height) / 25)
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin,
        labelSize))

# display titles on learn phonology menu
def displayPhonologyTitles(canvas, data):
    canvas.create_text(data.width / 2, data.height / 10, 
    text="Syllable Structure", font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 4, data.height / 3, text="Consonants", 
    font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width * 3 / 4, data.height / 3, text="Vowels", 
    font = "Ariel " + str(int(data.height / 20)))

# displays phonology rules
def drawLearnPhonology(canvas, data):
    data.buttons, syllable = [], []
    displayPhonologyTitles(canvas, data)
    sylPath = "languages/" + data.langName + "/syllableStructure.txt"
    syl = readFile(sylPath).split(", ")
    for i in range(3):
        if i == 0:
            for i in range(int(syl[i])): syllable += ["C"]
        if i == 1:
            for i in range(int(syl[i])): syllable += ["V"]
        if i == 2:
            for i in range(int(syl[i])): syllable += ["C"]
    syllable = "".join(syllable)
    canvas.create_text(data.width / 2, data.height / 5, text=syllable,
    font = "Ariel " + str(int(data.height / 20)), fill="gray")
    conPath = "languages/" + data.langName + "/legalConsonants.txt"
    vowPath = "languages/" + data.langName + "/legalVowels.txt"
    con, vow = readFile(conPath), readFile(vowPath)
    canvas.create_text(data.width / 4, data.height / 2, text=con, 
    font = "Ariel " + str(int(data.width / 75)), fill="gray")
    canvas.create_text(data.width * 3 / 4, data.height / 2, text=vow, 
    font = "Ariel " + str(int(data.width / 75)), fill="gray")
    backButton(canvas, data)

# displays titles 
def displayLearnMorphologyTitles(canvas, data):
    canvas.create_text(data.width / 2, data.height / 10, text="Genders", 
    font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 5, data.height / 6, text="Masculine", 
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width / 2, data.height / 6, text="Feminine",
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width * 4 / 5, data.height / 6, text="Neuter",
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width / 2, data.height / 4, text="Pronouns",
    font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 5, data.height / 3, text="First Person", 
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width / 2, data.height / 3, text="Second Person",
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width * 4 / 5, data.height / 3, text="Third Person",
    font = "Ariel " + str(int(data.height / 50)))
    displayDeterminerTitles(canvas, data)

# displays determiner titles
def displayDeterminerTitles(canvas, data):
    labelSize = int(data.height / 50)
    canvas.create_text(data.width / 2, data.height / 2, text="Determiners",
    font = "Ariel " + str(labelSize))
    canvas.create_text(data.width / 3, data.height * 3 / 5, text="Indefinite", 
    font = "Ariel " + str(labelSize))
    canvas.create_text(data.width * 2 / 3, data.height * 3 / 5, text="Definite", 
    font = "Ariel " + str(labelSize))
    canvas.create_text(data.width / 3, data.height * 3 / 5 + labelSize, 
    text="Masculine, Feminine, Neuter", 
    font = "Ariel " + str(labelSize))
    canvas.create_text(data.width * 2 / 3, data.height * 3 / 5 + labelSize, 
    text="Masculine, Feminine, Neuter", 
    font = "Ariel " + str(labelSize))
    
# displays noun morphology rules
def displayLearnNounRules(canvas, data):
    labelSize = int(data.height / 50)
    genderConj = ["", "", ""]
    nounsPath = "languages/" + data.langName + "/nounConjugation.txt"
    nouns = readFile(nounsPath)
    nouns = nouns.split("\n")
    place, gender, nominative, accusative, dative, genitive, plurality = nouns
    gender = gender[1:-1].split(", ")
    for i in range(len(gender)): gender[i] = gender[i][1:-1]
    place = int(place)
    if place == -1 or len(gender) == 1:
        genderConj = ["", "", ""]
    elif place == 0: 
        for i in range(len(gender)): genderConj[i] = "-" + gender[i]
    elif place == 1:
        for i in range(len(gender)): genderConj[i] = gender[i] + "-"
    # draw noun conjugation rules
    canvas.create_text(data.width / 5, data.height / 5, text=genderConj[0], 
    font = "Ariel " + str(labelSize), fill="gray")
    canvas.create_text(data.width / 2, data.height / 5, text=genderConj[1],
    font = "Ariel " + str(labelSize), fill="gray")
    canvas.create_text(data.width * 4 / 5, data.height / 5, text=genderConj[2],
    font = "Ariel " + str(labelSize), fill="gray")
    
# displays determiners and pronouns
def displayLearnDeterminers(canvas, data):
    determinersPath = "languages/" + data.langName + "/determiners.txt"
    determiners = readFile(determinersPath)
    determiners = determiners.splitlines()
    pronouns = determiners[-1]
    pronouns = pronouns[1:-1].split(", ")
    indefDet, defDet = determiners[0][1:-1], determiners[1][1:-1]
    labelSize = int(data.height / 50)
    for i in range(len(pronouns)): pronouns[i] = pronouns[i][1:-1]
    # draw pronouns
    canvas.create_text(data.width / 5, data.height / 2.5, text=pronouns[0], 
    font = "Ariel " + str(labelSize), fill="gray")
    canvas.create_text(data.width / 2, data.height / 2.5, text=pronouns[1],
    font = "Ariel " + str(labelSize), fill="gray")
    canvas.create_text(data.width * 4 / 5, data.height / 2.5, text=pronouns[2],
    font = "Ariel " + str(labelSize), fill="gray")    
    # draw determiners
    canvas.create_text(data.width / 3, data.height * 3 / 5 + labelSize * 3,
    text=indefDet, font = "Ariel " + str(labelSize), fill="gray")
    canvas.create_text(data.width * 2 / 3, data.height * 3 / 5 + labelSize * 3,
    text=defDet, font = "Ariel " + str(labelSize), fill="gray")

    
# displays morphology rules
def displayLearnMorphologyRules(canvas, data):
    displayLearnNounRules(canvas, data)
    displayLearnDeterminers(canvas, data)
    
# displays morphology menu    
def drawLearnMorphology(canvas, data):
    data.buttons = []
    displayLearnMorphologyTitles(canvas, data)
    displayLearnMorphologyRules(canvas, data)
    buttonNames = ["back", "lexicon"]
    sideMargin = data.width / 5
    bottomMargin = data.height / 10
    buttonHeight = min(data.width, data.height) / 10
    buttonWidth = (data.width - sideMargin * 2) / len(buttonNames)
    labelSize = int(min(data.width, data.height) / 25)
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin,
        labelSize))

# finds part of speech
def findPos(pos):
    if pos == "noun": pos = "(n)"
    elif pos == "adverb": pos = "(adv)"
    elif "verb" in pos: pos = "(v)"
    elif pos == "adjective": pos = "(adj)"
    elif pos == "quantifier": pos = "(quant)"
    elif pos == "question": pos = "(ques)"
    elif pos == "conjunction": pos = "(conj)"
    elif pos == "preposition": pos = "(prep)"
    elif pos == "expression": pos = "(exp)"
    return pos

# displays all words and their translations
def drawLearnLexicon(canvas, data):
    data.buttons = []
    # draw [word, part of speech, translation] (not including pronouns, 
    # determiners)
    lexiconPath = "languages/" + data.langName + "/lexicon.txt"
    lexicon = readFile(lexiconPath)
    lexicon = lexicon.splitlines()
    lexiconLen = len(lexicon)
    margin = 5
    for i in range(5):
        start = int(i * lexiconLen / 5)
        end = int((i + 1) * lexiconLen / 5)
        if end > lexiconLen: end = lexiconLen
        for j in range(start, end):
            wordInfo = lexicon[j].split("\t")
            pos = wordInfo[2]
            pos = findPos(pos)
            canvas.create_text(margin, 15 + j%(lexiconLen/5) * 11, anchor="nw",
            text=wordInfo[0]+"\t"+wordInfo[1]+pos, font="Ariel 10", fill="gray")
        margin += data.width / 5
    bottomMargin, sideMargin = data.height / 10, 20
    buttonHeight = int(data.height / 10)
    labelSize = int(min(data.width, data.height) / 25)
    backButton(canvas, data)

# displays titles
def displayLearnSyntaxTitles(canvas, data):
    canvas.create_text(data.width / 2, data.height / 10,
    text="Sentence Structure", font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 2, data.height / 3, text="Tenses",
    font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 5, data.height / 2, text="Past", 
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width / 2, data.height / 2, text="Present (non-past)", 
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width * 4 / 5, data.height / 2, text="Future",
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width / 2, data.height * 2 / 3, text="Cases",
    font = "Ariel " + str(int(data.height / 20)))
    canvas.create_text(data.width / 6, data.height * 0.7, text="Plural", 
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width * 2 / 6, data.height * 0.7, text="Nominative", 
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width * 3 / 6, data.height * 0.7, text="Accusative", 
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width * 4/ 6, data.height * 0.7, text="Dative", 
    font = "Ariel " + str(int(data.height / 50)))
    canvas.create_text(data.width * 5/ 6, data.height * 0.7, text="Genitive", 
    font = "Ariel " + str(int(data.height / 50)))
    
# displays sentence structure
def displayLearnSentenceStructure(canvas, data):
    sentPath = "languages/" + data.langName + "/sentenceStructure.txt"
    sent = readFile(sentPath)
    sent = list(sent)
    struct = []
    for i in range(3):
        if sent[i] == "v": struct += ["verb"]
        elif sent[i] == "s": struct += ["subject"]
        elif sent[i] == "o": struct += ["object"]
    struct = " ".join(struct)
    canvas.create_text(data.width / 2, data.height / 5, text=struct, 
    font = "Ariel " + str(int(data.height / 50)), fill="gray")
    
# displays tense rules
def displayLearnTenseRules(canvas, data):
    tensePath = "languages/" + data.langName + "/tenseConjugation.txt"
    tense = readFile(tensePath)
    tense = tense.splitlines()
    tenseConj = ["", "", ""]
    place, tense = tense[0], tense[1][1:-1]
    tenses = tense.split(", ")
    if int(place) == 0: 
        for i in range(len(tenses)): tenseConj[i] = tenses[i][1:-1] + "-"
    else:
        for i in range(len(tenses)): tenseConj[i] = "-" + tenses[i][1:-1]
    canvas.create_text(data.width / 5, data.height / 1.75, text=tenseConj[0], 
    font = "Ariel " + str(int(data.height / 50)), fill="gray")
    canvas.create_text(data.width / 2, data.height / 1.75, text=tenseConj[1], 
    font = "Ariel " + str(int(data.height / 50)), fill="gray")
    canvas.create_text(data.width * 4 / 5, data.height / 1.75, text=tenseConj[2],
    font = "Ariel " + str(int(data.height / 50)), fill="gray")
    
# displays case rules
def displayLearnCaseRules(canvas, data):
    nounPath = "languages/" + data.langName + "/nounConjugation.txt"
    noun = readFile(nounPath)
    place = noun[0]
    noun = noun.splitlines()[2:]
    for i in range(len(noun)): noun[i] = noun[i][2:-2]
    nounConj = ["", "", "", "", ""]
    if place == "0":
        for i in range(len(nounConj)): nounConj[i] = noun[i] + "-"
    elif place == "1":
        for i in range(len(nounConj)): nounConj[i] = "-" + noun[i]
    canvas.create_text(data.width / 6, data.height * 0.75, text=nounConj[4], 
    font = "Ariel " + str(int(data.height / 50)), fill="gray")
    canvas.create_text(data.width * 2 / 6, data.height * 0.75, text=nounConj[0], 
    font = "Ariel " + str(int(data.height / 50)), fill="gray")
    canvas.create_text(data.width * 3 / 6, data.height * 0.75, text=nounConj[1], 
    font = "Ariel " + str(int(data.height / 50)), fill="gray")
    canvas.create_text(data.width * 4/ 6, data.height * 0.75, text=nounConj[2], 
    font = "Ariel " + str(int(data.height / 50)), fill="gray")
    canvas.create_text(data.width * 5/ 6, data.height * 0.75, text=nounConj[3], 
    font = "Ariel " + str(int(data.height / 50)), fill="gray")

# displays syntax rules
def drawLearnSyntax(canvas, data):
    data.buttons = []
    displayLearnSyntaxTitles(canvas, data)
    displayLearnSentenceStructure(canvas, data)
    displayLearnTenseRules(canvas, data)
    displayLearnCaseRules(canvas, data)
    backButton(canvas, data)

### Playing Menu ###

# menu allows player to choose game
def drawPlayMenu(canvas, data):
    data.buttons = []
    buttonNames = ["back", "game"]
    sideMargin = data.width / 5
    bottomMargin = data.height / 10
    buttonHeight = min(data.width, data.height) / 10
    buttonWidth = (data.width - sideMargin * 2) / len(buttonNames)
    labelSize = int(min(data.width, data.height) / 25)
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin,
        labelSize))
        
# menu displays all saved languages for game
def drawGameMenu(canvas, data):
    canvas.create_text(data.width / 2, data.height / 10, text="Choose language", 
    font = "Ariel " + str(int(data.height / 10)))
    numLanguages = len(os.listdir("languages"))
    data.buttons = []
    sideMargin = data.width / 10
    topMargin = data.height / 5
    bottomMargin = data.height / 10
    labelSize = int(min(data.width, data.height) / 25)
    buttonHeight = data.height / 25
    backButtonHeight = data.height / 10
    smallLabelSize = int(buttonHeight)
    backSideMargin = data.width / 3
    for i in range(numLanguages):
        data.buttons += [display.Button(os.listdir("languages")[i], sideMargin, 
        topMargin + buttonHeight * i, data.width - sideMargin, 
        topMargin + buttonHeight * (i + 1), smallLabelSize)]
    backButton(canvas, data)
    
# menu displays all games
def drawGameChoiceMenu(canvas, data):
    data.buttons = []
    canvas.create_text(data.width / 2, data.height / 10, text="Choose game", 
    font = "Ariel " + str(int(data.height / 10)))
    buttonNames = ["back", "game1", "game2"]
    sideMargin = data.width / 5
    bottomMargin = data.height / 10
    buttonHeight = min(data.width, data.height) / 10
    buttonWidth = (data.width - sideMargin * 2) / len(buttonNames)
    labelSize = int(min(data.width, data.height) / 25)
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin,
        labelSize))

def drawGetInput(canvas, data):
    height = 20
    width = 50
    margin = 30
    canvas.create_rectangle(0, data.height - margin - height, data.width, 
                            data.height - margin, fill="white")
    canvas.create_text(data.width / 2, data.height - margin - height / 2,
                        text=data.input)

def drawScore1(canvas, data):
    canvas.create_text(data.width//2 - 200, data.height - 100, 
    text = 'Score: ' + str(data.score1),
    font = 'Arial 30 bold',
    fill = 'grey')
    
def drawLives1(canvas, data):
    canvas.create_text(data.width//2 + 200, data.height - 100, 
    text = 'Lives: ' + str(data.lives1),
    font = 'Arial 30 bold',
    fill = 'grey')

# function draws game1
def drawGameScreen1(canvas, data):
    height = 20
    width = 50
    margin = 30
    data.buttons = [display.Button("back", 0, data.height - margin, 
    data.width, data.height, int(margin * 2 / 3))]
    canvas.create_text(data.width / 2, 10, anchor="n",
    text="Type the meaning of the falling word in English and press enter.", 
    font="Ariel " + str(int(data.width / 75)))
    conLangGame.runGame(canvas, data)
    drawGetInput(canvas, data)
    drawScore1(canvas, data)
    drawLives1(canvas, data)
    
def drawScore2(canvas, data):
    canvas.create_text(data.width//2 - 200, data.height/10, 
    text = 'Score: ' + str(data.score2),
    font = 'Arial 30 bold',
    fill = 'grey')
    
def drawLives2(canvas, data):
    canvas.create_text(data.width//2 + 200, data.height/10, 
    text = 'Lives: ' + str(data.lives2),
    font = 'Arial 30 bold',
    fill = 'grey')
    
# function draws game2
def drawGameScreen2(canvas, data):
    height = 20
    width = 50
    margin = 30
    canvas.create_text(data.width / 2, 10, anchor="n",
    text="Use the left and right keys to guide the word to its part of speech.", 
    font="Ariel " + str(int(data.width / 75)))
    conLangGame2.runGame(canvas, data)
    data.buttons = [display.Button("back", 0, data.height - margin, 
    data.width, data.height, int(margin * 2 / 3))]
    drawScore2(canvas, data)
    drawLives2(canvas, data)
    
### Main Menu ###

# menu allows user to choose to create a new language, learn a saved language, 
# or play games 
def drawMainMenu(canvas, data):
    buttonNames = ["create", "learn", "play"]
    data.buttons = []
    sideMargin = data.width / 5
    bottomMargin = data.height / 10
    buttonHeight = min(data.width, data.height) / 10
    buttonWidth = (data.width - sideMargin * 2) / len(buttonNames)
    labelSize = int(min(data.width, data.height) / 25)
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin,
        labelSize))
    canvas.create_text(data.width / 2, data.height / 5, text="Welcome!", 
    font = "Ariel " + str(int(data.height / 10)))

### Draw Menu Based on Mode ###

def drawMenu(canvas, data):
    if data.mode == "welcomeScreen": drawMainMenu(canvas, data)
    elif data.mode == "create": drawCreateMenu(canvas, data)
    elif data.mode == "custom": drawUserCreateMenu(canvas, data)
    elif data.mode == "phonology" and data.prevModes[-2] == "custom":
        drawUserPhonologyMenu(canvas, data)
    elif data.mode == "morphology" and data.prevModes[-2] == "custom":
        drawUserMorphologyMenu(canvas, data)
    elif data.mode == "syntax" and data.prevModes[-2] == "custom":
        drawUserSyntaxMenu(canvas, data)
    elif data.mode == "random" or data.mode == "done":
         drawComputerCreateMenu(canvas, data)
    elif data.mode == "learn": drawLearnAllMenu(canvas, data)
    elif data.mode == "phonology": drawLearnPhonology(canvas, data)
    elif data.mode == "morphology": drawLearnMorphology(canvas, data)
    elif data.mode == "lexicon": drawLearnLexicon(canvas, data)
    elif data.mode == "syntax": drawLearnSyntax(canvas, data)
    elif data.mode == "play": drawPlayMenu(canvas, data)
    elif data.mode == "game": drawGameMenu(canvas, data)
    elif data.mode == "gameScreen": drawGameChoiceMenu(canvas, data)
    elif data.mode == "game1": drawGameScreen1(canvas, data)
    elif data.mode == "game2": drawGameScreen2(canvas, data)
    else: drawLearnLangMenu(canvas, data)

def redrawAll(canvas, data):
    drawMenu(canvas, data)
    display.Menu(data.buttons).draw(canvas)

####################################
# Use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(900, 600)