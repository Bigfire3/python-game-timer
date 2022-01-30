import tkinter as tk
import psutil
import time
import threading
from win10toast import ToastNotifier
import sys
import subprocess

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

def checkProcess(processName):
    count = 0
    for proc in psutil.process_iter():
        try:
            if processName in proc.name():
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return count
                

class WindowThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        global threadStart
        global pauseTimer
        self.window = tk.Tk()
        self.window.title("GameTimer")
        self.label = tk.Label(self.window, text = "00:00:00", font = ("Arial", 25))
        self.label.pack()

        self.button = tk.Button(self.window, text = "Pause", command = self.buttonAction)
        self.button.pack()

        self.label.after(500, self.updateLabel)
        self.window.mainloop()
        threadStart = False
        pauseTimer = False
    
    def updateLabel(self):
        global elapsedSeconds
        h, m, s = secondsToClock(elapsedSeconds)
        self.label.config(text = clockToString(h, m , s))
        self.label.after(500, self.updateLabel)

    def buttonAction(self):
        global pauseTimer
        if pauseTimer == False:
            self.button.config(text = "Weiter")
            pauseTimer = True
        else:
            pauseTimer = False
            self.button.config(text = "Pause")

elapsedSeconds = 0
oldSeconds = 0
runningTimer = False
threadStart = False
oldGameSeconds = 0
gamePadEnable = True
pauseTimer = False

toaster = ToastNotifier()

if checkProcess("GameTimer.exe") > 2:
    sys.exit()

else:
    while True:
        rlProc = checkProcess("RocketLeague.exe")
        wzProc = checkProcess("ModernWarfare.exe")
        if (wzProc > 0 or rlProc > 0) and pauseTimer == False:
            if runningTimer == False:
                startTime = time.time()
                runningTimer = True
            elapsedSeconds = int(time.time() - startTime) + oldSeconds
            if rlProc > 0 and gamePadEnable == False:
                try:
                    subprocess.call('pnputil /enable-device "HID\VID_054C&PID_0CE6&MI_03\8&AB95EF8&0&0000"', shell = True)
                    toaster.show_toast("GameTimer", "PS5-Controller aktiviert", icon_path = "", duration = 5)
                    gamePadEnable = True
                except:
                    toaster.show_toast("GameTimer", "PS5-Controller nicht verbunden", icon_path = "", duration = 5)
            #print (elapsedSeconds)
        else:
            if gamePadEnable and rlProc < 1:
                try:
                    subprocess.call('pnputil /disable-device "HID\VID_054C&PID_0CE6&MI_03\8&AB95EF8&0&0000"', shell = True)
                    toaster.show_toast("GameTimer", "PS5-Controller deaktiviert", icon_path = "", duration = 5)
                    gamePadEnable = False
                except:
                    toaster.show_toast("GameTimer", "PS5-Controller konnte nicht deaktiviert werden", icon_path = "", duration = 5)
            oldSeconds = elapsedSeconds
            runningTimer = False
        if checkProcess("GameTimer.exe") > 2 and threadStart == False:
            WindowThread().start()
            threadStart = True
        if elapsedSeconds > (oldGameSeconds + 1800):
            h, m, s = secondsToClock(elapsedSeconds)
            toaster.show_toast("GameTimer", "Du spielst schon " + clockToString(h, m, s) + "!", icon_path = "", duration = 3)
            oldGameSeconds = elapsedSeconds
