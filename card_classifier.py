###imports###
import os
import torch
import sys
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


def check_cuda():
    if not torch.cuda.is_available():
        print("[ERROR] CUDA is not available. Training will fall back to CPU.")
        sys.exit(1)
    else:
        print(f"[INFO] CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")

def train_model_if_needed():
    """checks if model exists, if not trains a new one and stores in the git folder"""

    # should work for both of us
    model_path = "Models/training/weights/best.pt"

    if os.path.exists(model_path):
        print(f"[INFO] Model already trained. Using existing model at: {model_path}")
        return model_path

    print("[INFO] Model not found. Starting training on GPU...")
    model = YOLO("yolo11n.pt")
    model.train(
        # add config for both of us here
        data="C:/Users/mfouc/OneDrive/Desktop/Clash Royal Detection V2.v1i.yolov8/data.yaml",
        epochs=100,
        conf=0.2,
        project="Models",   # Store everything inside the Models folder
        name="training",
        device="cuda"
    )
    print("[INFO] Training complete.")
    return model_path

def run_inference(model_path):
    """ this is where the prediction happens and the inference based on the model trained above"""


    print("[INFO] Running inference on GPU...")
    model = YOLO(model_path)

    results = model(
        # add config for both of us
        "C:/Users/mfouc/OneDrive/Desktop/GameData/testData/image_1747621634.png",
        conf=0.2,
        iou=0.6,
        save=True,
        project="Models/Results",   # Save inference results in Models/Results
        name="inference_run1",
        device="cuda"
    )
    print("[INFO] Inference complete. Results saved.")

def use_Pre_Trained():
    check_cuda()
    model_path = train_model_if_needed()
    run_inference(model_path)


if __name__ == "__main__":
    #collect_images(2)
    use_Pre_Trained()