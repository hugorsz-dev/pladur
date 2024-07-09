# DEPENDENCIES
import os
import pygetwindow
import pyautogui
import shutil
import datetime
import win32gui
import win32con
import time
import pytesseract
import json
import requests
from datetime import datetime
from PIL import Image

# INTRODUCTION

print(r" ____  _           _ ")
print(r"|  _ \| | __ _  __| |_   _ _ __ ")
print(r"| |_) | |/ _` |/ _` | | | | '__| ")
print(r"|  __/| | (_| | (_| | |_| | | ")
print(r"|_|   |_|\__,_|\__,_|\__,_|_| ")

print("Consult your scenes with AI!")
print("")

# CONFIGURATIONS

with open("headers.json", 'r') as file_1:
    header_config = json.load(file_1)

with open("config.json", 'r') as file_2:
    config = json.load(file_2)

"""
Pytesseract is the program that converts on-screen text into a readable format: that is, from image to text.
To do this, you need to have the program installed in a known location, which should be listed in the config.json file.
https://github.com/UB-Mannheim/tesseract/wiki

And within that folder, in "tessdata" should be the "spa.traineddata" file, downloadable at:
https://github.com/tesseract-ocr/tessdata
"""

# PYTESSERACT INSTALLATION

pytesseract.pytesseract.tesseract_cmd = config["tesseract_path"]

"""
Determines the existence of the game window and returns its name. If it does not exist,
it will be considered that the game is NOT running and orders the
system to stop.
"""

def game_window():
    window_names = pygetwindow.getAllTitles()
    for name in window_names:
        if config["window_reference"] in name:
            return name

    print(f'[{datetime.now().strftime("%H:%M:%S")}] > No game window open')
    return False

"""
Takes a screenshot of the specified window.
"""

def screenshot(window_title=None, file_path="tmp.png"):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            time.sleep(1)
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            im.save(file_path)
            return im
        else:
            print(f'[{datetime.now().strftime("%H:%M:%S")}] > Stopping screenshot: window is not running.')
    else:
        im = pyautogui.screenshot()
        im.save(file_path)
        print(f'[{datetime.now().strftime("%H:%M:%S")}] > Text successfully collected.')
        return im

""" 
Makes a query to RAPIDAPI
"""

def query_rapid_api(query):
    url = "https://chatgpt-best-price.p.rapidapi.com/v1/chat/completions"

    headers = header_config

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()['choices'][0]['message']['content']

# MAIN LOOP

queryCounter = 0
makeQuery = False
query = ""

while game_window():
    time.sleep(3)
    
    try:
        # Take the screenshot.
        screenshot(game_window())

        # Interpret the log
        image = Image.open('tmp.png')
        log = pytesseract.image_to_string(image, lang='spa')

        # Post-process the log to compress it and eliminate possible garbage records.
        lines = log.split('\n')
        non_space_lines = [line for line in lines if not line.isspace() and len(line.strip()) >= 5]

        # Insert query
        query = query + ' '.join(non_space_lines)
        makeQuery = True

    except:
        if queryCounter > 10:
            queryCounter = 0
            query = ""
            makeQuery = False
            
        if makeQuery:
            print("Making summary query:")
            print(query_rapid_api(config["context"] + query))
            
            query = ""
            makeQuery = False
