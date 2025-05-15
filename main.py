# main file to test things 

from Screen_capture import capture_bluestacks
from info_extractor import extract 
import time

pyautogui.moveTo(100, 200)  # move mouse to x=100, y=200
pyautogui.click()           # default is left-click

start_time = time.perf_counter()

#just end after a minute for now
def gameOver(time):
    if (time - start_time) > 5:
        return 1

while not gameOver(time.perf_counter()):
    print("game not over")
    capture_bluestacks()
    extract()

