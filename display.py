# Sophia Ho
# Display Class (15-112 Fall 2018 Term Project)
# AndrewID: swho
# Recitation: P

from tkinter import *

class Menu(object):
    def __init__(self, buttons):
        self.buttons = buttons
    def draw(self, canvas):
        for button in self.buttons:
            canvas.create_rectangle(button.x0, button.y0, button.x1, button.y1, 
            fill=button.color)
            midX, midY = (button.x0 + button.x1) / 2, (button.y0 + button.y1) / 2
            canvas.create_text(midX, midY, text=button.name, font = "Ariel " + 
            str(button.labelSize))

class Button(object):
    def __init__(self, name, x0, y0, x1, y1, labelSize, isClicked=False):
        self.name = name
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.isClicked = isClicked
        self.labelSize = labelSize
        self.color = "lightblue"
    def __repr__(self):
        return self.name
    def click(self):
        self.isClicked = not self.isClicked
        if self.isClicked: self.color = "yellow"
        else: self.color = "lightblue"
        