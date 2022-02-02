from tkinter import *
from win10toast import ToastNotifier
import psutil
import time
import datetime

rlRunning = False
wzRunning = False
endGame = False
setGameSeconds = 3600 # in minutes
isGameTime = 0
rocketLeagueTime = 0
warzoneTime = 0
runTimer = False

toaster = ToastNotifier()

def plusButton():
    global setGameSeconds
    setGameSeconds += 60
    
def minusButton():
    global setGameSeconds
    setGameSeconds -= 60

def secondsToClock(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = (seconds % 3600) % 60
    return h, m, s

def clockToString(h, m, s):
    if h < 10:
        hString = "0" + str(h)
    else:
        hString = str(h)
    if m < 10:
        mString = "0" + str(m)
    else:
        mString = str(m)
    if s < 10:
        sString = "0" + str(s)
    else:
        sString = str(s)
    clockString = hString + ":" + mString + ":" + sString
    return clockString

def main():
    global gameTimeLabel
    hSet, mSet, sSet = secondsToClock(setGameSeconds)
    allTimeLabel.config(text = "00:00:00/" + clockToString(hSet, mSet, sSet))
    """if "Time.exe" in (p.name() for p in psutil.process_iter()):
        #if runTimer == False:
        #    rlStartTime = time.time()
        #    rlRunning = True
        #    runTimer = True
    #if "ModernWarfare.exe" in (p.name() for p in psutil.process_iter()): # RocketLeague.exe
        #if runTimer == False:
            #wzStartTime = time.time()
            #wzRunning = True
            #runTimer = True
    else:
        rlRunning = False
        wzRunning = False
        runTimer = False"""
    
    if rlRunning:
        rlElapsedSeconds = int(time.time()) - int(rlStartTime)
        rlH, rlM, rlS = secondsToClock(rlElapsedSeconds)

        gameTimeLabel.config(text = "RocketLeague: " + clockToString(rlH, rlM, rlS) + "\nWarzone: ")

    if wzRunning:
        pass
        #toaster.show_toast("GameTimer", "Hör auf zu spielen!!! Du spielst schon eine halbe Stunde")
    #gameTimeLabel.after(1, main)

window = Tk()
window.title("GameTime")

h, m, s = secondsToClock(setGameSeconds)
allTimeLabel = Label(window, text = "00:00:00/" + clockToString(h, m, s), font = ("arial", 20))
gameTimeLabel = Label(window, text = "RocketLeague: " + "00:00:00" + "\nWarzone: " + "00:00:00", font = ("arial", 18))
plusButton = Button(window, text = "+", width = 3, command = plusButton, font = ("arial", 20))
minusButton = Button(window, text = "-", width = 3, command = minusButton, font = ("arial", 20))

plusButton.grid(row = 0, column = 1, padx = 50)
minusButton.grid(row = 1, column = 1, padx = 50)
allTimeLabel.grid(row = 0, column = 0)
gameTimeLabel.grid(row = 1, column = 0)

while True:
    main()
window.mainloop()
