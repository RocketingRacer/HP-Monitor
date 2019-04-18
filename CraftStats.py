import backend
import pygame
import tkinter as tk
pygame.init()
title = ("Arial", 44)
header =("Arial", 25)
plain = ("Arial", 14)
class PlaneInfo:
    def __init__(self):
        print("WIP")
class Bar:
    def __init__(self):
        print("WIP")


class Overlay:
    def parseColor(self,color):
        letters = color[-6:]
        r = int(letters[:2],16)
        g = int(letters[2:4],16)
        b = int(letters[4:6],16)
        return(r,g,b)
    def __init__(self,size,background,Acolor,Bcolor):
        self.background = self.parseColor(background)
        self.Acolor = self.parseColor(Acolor)
        self.BColor = self.parseColor(Bcolor)
        #print(self.background)
        self.window = pygame.display.set_mode(size,pygame.RESIZABLE)
        self.window.fill(self.background)
        pygame.display.flip()
        self.planes = []
        self.conn = backend.Utilitys.getconn()
        self.commandQueue = []
        self.data = backend.gameLoop(self.conn,self.commandQueue)
        self.update()
    def update(self):
        planes = self.data.update(self.commandQueue[])

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        #print(self.grid_size())

    def createWidgets(self):
        self.TitleLabel = tk.Label(text="CraftStats",font = title,fg = "#FF0000")
        self.TitleLabel.grid(row = 0,columnspan = 3)

        self.colorLabel = tk.Label(text="Colors",font = header)
        self.colorLabel.grid(row = 1,column = 0,sticky = "w")
        self.colorLabel.grid(padx = 10, pady = 10)

        self.tcLabel = tk.Label(text="TextColor  A:",font = plain)
        self.tcLabel.grid(row = 2,column = 0,sticky = "w")
        self.tcLabel.grid(padx = 10, pady = 10)

        self.ForegroundBoxA = tk.Entry(font = plain,)
        self.ForegroundBoxA.grid(row = 2,column = 1,sticky = "w")
        self.ForegroundBoxA.grid(padx = 10, pady = 10)
        self.ForegroundBoxA.insert(0,"#BF0000")

        self.tcLabelB = tk.Label(text="B:",font = plain)
        self.tcLabelB.grid(row = 3,column = 0,sticky = "e")
        self.tcLabelB.grid(padx = 10, pady = 10)

        self.ForegroundBoxB = tk.Entry(font = plain)
        self.ForegroundBoxB.grid(row = 3,column = 1,sticky = "w")
        self.ForegroundBoxB.grid(padx = 10, pady = 10)
        self.ForegroundBoxB.insert(0,"#0000BF")

        self.backColorLabel = tk.Label(text="Background",font = plain)
        self.backColorLabel.grid(row = 4,column = 0,sticky = "w")
        self.backColorLabel.grid(padx = 10, pady = 10)

        self.startButton = tk.Button(self, text="START!", command = self.start)
        self.startButton.grid(row = 6,column = 0)

        self.BackgroundBox = tk.Entry(font = plain)
        self.BackgroundBox.grid(row = 4,column = 1,sticky = "w")
        self.BackgroundBox.grid(padx = 10, pady = 10)
        self.BackgroundBox.insert(0,"#00FF00")



    def start(self):
        overlay = Overlay((500,500),self.BackgroundBox.get(),self.ForegroundBoxA.get(),self.ForegroundBoxB.get())

pygame.init()
background = (255,255,255)
TitleColor = (0,0,0)


def main():
    app = Application()
    app.master.title('Craft Stat Overlay')
    app.mainloop()


if __name__ == "__main__":
    main()
