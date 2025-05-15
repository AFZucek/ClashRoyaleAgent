from PIL import ImageGrab
# py -3.11 -m pip install pygetwindow
import pygetwindow as gw
import pyautogui
import time
import os

#moved path creation outside of function
path = os.path.join("data", "TestCaptures", "testscreen.png")
os.makedirs(os.path.dirname(path), exist_ok=True)

def capture_bluestacks(win):
    """take screen shot of blue stacks window"""

    x, y, w, h = win.left, win.top, win.width, win.height

    img = pyautogui.screenshot(region=(x, y, w, h))

    # save image
    img.save(path)
    return img


def main():
    """main function"""
    im = capture_bluestacks()
    print("Captured size:", im.size)


if __name__ == "__main__":
    main()