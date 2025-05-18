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


#grab pre made model
from ultralytics import YOLO

"""
# Parameters
DATA_DIR = "C:/Users/mfouc/OneDrive/Desktop/Clash_Cards_Data/" # error here ??
BATCH_SIZE = 32 # depends on cpu/gpu
NUM_EPOCHS = 10 # passes over data
IMG_SIZE = 128
MODEL_PATH = "Models/classifier.pth"
"""

if os.getlogin() == 'mfouc':
    PATH = "C:/Users/mfouc/OneDrive/Desktop/GameData/Arena_1"
else:
    PATH = "D:/ClashData/TestScreenshots/Arena_1/1" #update num for each game

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



    for i in range(90):
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


def train():

    # Load a pretrained YOLO model (recommended for training)
    model = YOLO("yolo11n.pt")

    # Train the model using the 'coco8.yaml' dataset for 3 epochs
    results = model.train(data="D:/ClashData/CNNYOLO8Data/data.yaml", epochs=3)

    # Evaluate the model's performance on the validation set
    results = model.val()

    # Perform object detection on an image using the model
    results = model("D:/ClashData/CNN_Test_Images/image_1747453019.png", save = True)

    # Export the model to ONNX format
    success = model.export(format="onnx")

#collect_images(2)

train()