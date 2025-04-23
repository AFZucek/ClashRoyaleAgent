# extract all the necessary information on a given game state (image)

#### IMPORTS ####
from PIL import Image
import pytesseract


def extract(image):
    """Puts together information extracted by OCR in the game"""

    # time left in seconds
    time_remaining = get_time(image)
    
    # Enemy tower information

    # Cards on screen, oponent/user

    # User tower information

    # Cards in hand w/their information

def get_time(image):
    """get Image from top right, uses OCR for the time in seconds"""

    # Extract Top Right

    # Run OCR
    time_string = pytesseract.image_to_string(image)
    minutes, seconds = map(int, time_string.split(":"))

    return minutes * 60 + seconds