# main file to test things 

from Screen_capture import capture_bluestacks
from info_extractor import extract 
import time
from Screen_capture import pyautogui
import pygetwindow as gw

#initialize window to bring bluestacks to the front later
window = gw.getWindowsWithTitle("BlueStacks")

if not window:
    raise Exception("BlueStacks window not found")
win = window[0]

start_time = time.perf_counter()



#Later change, to end game when actual time runs out or 3 crown
def gameOver(time):
    """
    Function that returns if the game is over given the time
    Later update to factor in game ending by 3 crown, overtime, ect. 
    """
    if (time - start_time) > 8: #should really be 180 for full game
        return 1



def start_training_battle():
    """
    Function to auto click to start training battle
    Currently only works with 4k full screen
    Later switch to constants to try to alter with screen size
    """
    # pop it to the front
    win.activate()
    time.sleep(0.03)  # give it a moment to come to front

    pyautogui.moveTo(2400, 250)  # move mouse to click menu
    pyautogui.click()           # default is left-click

    pyautogui.moveTo(2000, 780)  # move mouse to click training
    pyautogui.click()


    pyautogui.moveTo(2100, 1250)  # move mouse to click yes
    pyautogui.click()


def main():
    """
    main function
    """

    start_training_battle()
    time.sleep(5) # lets game load, update this later

    while not gameOver(time.perf_counter()):
        capture_bluestacks(win)
        extract()


if __name__ == "__main__":
    main()
