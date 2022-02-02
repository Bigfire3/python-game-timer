import tkinter as tk
import time
import psutil
from win10toast import ToastNotifier
import subprocess
import sys

elapsed_game_seconds = 0
old_game_seconds = 0
start_seconds = 0
last_notifier_seconds = 0
running_timer = True
toaster = ToastNotifier()

# transform e.g. int(16430) to "04:33:50"
def seconds_to_clock(seconds: int) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int((seconds % 3600) % 60)
    clock_list = [str(h).zfill(2), str(m).zfill(2), str(s).zfill(2)]
    clock_string = ":".join(clock_list)
    return clock_string

def check_process(process_name):
    count = 0
    for proc in psutil.process_iter():
        try:
            if process_name in proc.name():
                count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print("Process not found.")
    return count

def update_label():
    main()
    clock_text = seconds_to_clock(elapsed_game_seconds)
    # change label text
    time_label.config(text = clock_text)
    time_label.after(500, update_label)

def main():
    # look if rl or wz is running, return 1 if running
    rl_proc = check_process("RocketLeague.exe")
    wz_proc = check_process("ModernWarfare.exe")
    if rl_proc > 0 or wz_proc > 0:
        global elapsed_game_seconds, running_timer, old_game_seconds, start_seconds, last_notifier_seconds
        if running_timer == False:
            start_seconds = time.time()
            old_game_seconds = elapsed_game_seconds
            running_timer = True
            if rl_proc > 0:
                try:
                    subprocess.call('pnputil /enable-device "HID\VID_054C&PID_0CE6&MI_03\8&AB95EF8&0&0000"', shell = True)
                    toaster.show_toast("GameTimer", "PS5-Controller aktiviert", icon_path = "", duration = 5)
                except:
                    toaster.show_toast("GameTimer", "PS5-Controller nicht verbunden", icon_path = "", duration = 5)
        # increase total game seconds 
        elapsed_game_seconds = old_game_seconds + (time.time() - start_seconds)
        if elapsed_game_seconds > (last_notifier_seconds + 1800):
            toaster.show_toast("GameTimer", "Du spielst schon " + seconds_to_clock(elapsed_game_seconds) + "!", icon_path = "", duration = 5)
            last_notifier_seconds = elapsed_game_seconds
    else:
        if running_timer == True:
            running_timer = False
            try:
                subprocess.call('pnputil /disable-device "HID\VID_054C&PID_0CE6&MI_03\8&AB95EF8&0&0000"', shell = True)
                toaster.show_toast("GameTimer", "PS5-Controller deaktiviert", icon_path = "", duration = 5)
            except:
                toaster.show_toast("GameTimer", "PS5-Controller konnte nicht deaktiviert werden", icon_path = "", duration = 5)

if check_process("GameTimer.exe") > 2:
    sys.exit()

else:
    while True:
        main()
        if check_process("GameTimer.exe") > 2:
            # generate window
            window = tk.Tk()
            window.title("GameTimer")
            # generate label on window
            time_label = tk.Label(window, text = "")
            time_label.pack()
            # call method to update the label text first time
            time_label.after(500, update_label)
            # block while window is open
            window.mainloop()
        time.sleep(0.2)
