# Sophia Ho
# main.py (15-112 Fall 2018 Term Project)
# andrewID: swho
# Recitation: P

# Updated Animation Starter Code taken from 15-112 website

from tkinter import *
import display

####################################
# Display user interface 
####################################

def init(data):
    data.mode = "welcomeScreen"
    data.buttons = []

def mousePressed(event, data):
    print(event.x, event.y)
    for button in data.buttons:
        if (button.x0 <= event.x <= button.x1 and 
            button.y0 <= event.y <= button.y1):
            data.mode = button.name

def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def drawCreateMenu(canvas, data):
    pass
    
def drawLearnMenu(canvas, data):
    pass

def drawPlayMenu(canvas, data):
    pass

def drawMainMenu(canvas, data):
    buttonNames = ["create", "learn", "play"]
    data.buttons = []
    sideMargin = data.width / 5
    bottomMargin = data.height / 10
    buttonHeight = data.height / 10
    buttonWidth = data.width / 5
    for i in range(len(buttonNames)):
        data.buttons.append(display.Button(buttonNames[i], 
        sideMargin + i * buttonWidth, data.height - bottomMargin - buttonHeight, 
        sideMargin + (i + 1) * buttonWidth, data.height - bottomMargin))
    display.Menu(data.buttons).draw(canvas)

def drawMenu(canvas, data):
    if data.mode == "welcomeScreen": drawMainMenu(canvas, data)
    elif data.mode == "create": drawCreateMenu(canvas, data)
    elif data.mode == "learn": pass #drawLearnMenu(canvas, data)
    elif data.mode == "play": pass #drawPlayMenu(canvas, data)

def redrawAll(canvas, data):
    drawMenu(canvas, data)

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

run(500, 500)