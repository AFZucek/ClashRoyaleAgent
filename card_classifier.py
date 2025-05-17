###imports###
import os
"""
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
"""
from Screen_capture import pyautogui
import pygetwindow as gw
import time

"""
# Parameters
DATA_DIR = "C:/Users/mfouc/OneDrive/Desktop/Clash_Cards_Data/" # error here ??
BATCH_SIZE = 32 # depends on cpu/gpu
NUM_EPOCHS = 10 # passes over data
IMG_SIZE = 128
MODEL_PATH = "Models/classifier.pth"
"""


PATH = "C:/Users/mfouc/OneDrive/Desktop/GameData/Arena_1"

# error check for addy
if os.getlogin() != "mfouc":
    print("Set up a folder to store ALL data")
    exit


def collect_images(interval):
    """ watches clash royale games and takes images storing for data"""

    window = gw.getWindowsWithTitle("BlueStacks")

    if not window:
        raise Exception("BlueStacks window not found")
    win = window[0]


    win.activate()
    time.sleep(0.03)  

    pyautogui.moveTo(2400, 240)  # move mouse to click menu
    pyautogui.click() 
    pyautogui.moveTo(2000, 500)  # move mouse to click menu
    pyautogui.click()

    # start capturing
    time.sleep(10)



    for i in range(60):
        x, y, w, h = win.left, win.top, win.width, win.height

        img = pyautogui.screenshot(region=(x, y, w, h))

        crop_top_ratio, crop_bottom_ratio = 0.1422, 0.8605
        top_crop = int(win.height * crop_top_ratio)
        bot_crop = int(win.height * crop_bottom_ratio)

        cropped = img.crop((0, top_crop, win.width, bot_crop))

        # save image
        filename = f"image_{int(time.time())}.png"
        cropped.save(f"{PATH}/{filename}")
        time.sleep(interval)


collect_images(3)