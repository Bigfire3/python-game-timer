from tkinter import *
import psutil
import time

class GameTimer:
    def __init__(self, label):
        self.label = label
        self.elapsedSeconds = 0
        self.oldSeconds = 0
        self.runningTimer = False
        
    def timer(self):
        if "Time.exe" in (p.name() for p in psutil.process_iter()): # ModernWarfare.exe, RocketLeague.exe
            if self.runningTimer == False:
                self.startTime = time.time()
                self.runningTimer = True
            self.elapsedSeconds = int(time.time() - self.startTime) + self.oldSeconds
            self.label.config(text = str(self.elapsedSeconds))
            print (self.elapsedSeconds)
        else:
            self.oldSeconds = self.elapsedSeconds
            self.runningTimer = False
        
        self.label.after(1, self.timer)

while True:
    window = Tk()
    window.title = "GameTimer"

    time_label = Label(window, text = "00:00:00")
    time_label.pack()
    
    gameTimer = GameTimer(time_label)
    gameTimer.timer()
    window.mainloop()
