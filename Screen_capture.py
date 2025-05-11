from PIL import ImageGrab
# py -3.11 -m pip install pygetwindow
import pygetwindow as gw
import pyautogui
import time
import os


def capture_bluestacks():
    """take screen shot of blue stacks window"""

    window = gw.getWindowsWithTitle("BlueStacks")

    if not window:
        raise Exception("BlueStacks window not found")
    win = window[0]

    # pop it to the front
    win.activate()
    time.sleep(0.03)  # give it a moment to come to front

    x, y, w, h = win.left, win.top, win.width, win.height

    img = pyautogui.screenshot(region=(x, y, w, h))

    # save image
    path = os.path.join("data", "TestCaptures", "testscreen.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)
    return img


def main():
    """main function"""
    im = capture_bluestacks()
    print("Captured size:", im.size)


if __name__ == "__main__":
    main()