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
            button.draw(canvas)

class Button(object):
    def __init__(self, name, x0, y0, x1, y1, isClicked=False):
        self.name = name
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.isClicked = isClicked
    def click(self):
        self.isClicked = not self.isClicked
    def draw(self, canvas):
        if self.isClicked:
            color = "yellow"
        else:
            color = "lightblue"
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=color)
        midX, midY = (self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2
        canvas.create_text(midX, midY, text=self.name)