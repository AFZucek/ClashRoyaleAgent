# extract all the necessary information on a given game state (image)

#### IMPORTS ####
import os
from PIL import Image, ImageOps
import pytesseract
import cv2
import numpy as np
# load in the .env file
from dotenv import load_dotenv
load_dotenv()

# set up the pytesseract EXE 
TESSERACT_EXE_PATH = os.getenv("TESSERACT_EXE_PATH")



cv2.ocl.setUseOpenCL(True) #trying this to use open cl with amd gpu

def extract():
    """Puts together information extracted by OCR in the game"""

    # get image from folder

    dir = os.path.join(os.path.dirname(__file__) , "data/TestCaptures")
    image_path = os.path.join(dir, "testscreen.png")
    image = Image.open(image_path)

    #print(image.size)

    
    # Enemy tower information
    l, r = get_tower(image)
    print(f"Left Tower health: {l}")
    print(f"Right Tower health: {r}")

    get_cards(image)
    """
    # Cards on screen, oponent/user (OCR)
    c1, c2, c3, c4 = get_cards(image)
    print(f"Card 1: {c1}")
    print(f"Card 2: {c2}")
    print(f"Card 3: {c3}")
    print(f"Card 4: {c4}")
    """

    # User tower information

    # get elixir (optional)

    e = get_elixir(image)
    print(f"Elixir: {e}")

    # Cards in hand w/their information

    # return
    return l, r, e

def updateImageSize(img):
    width, height = img.size
    if width != 1185 or height != 2109:
        img = img.resize((1185, 2109), Image.LANCZOS)
        #img = img.crop((0, 30, img.width - 30, img.height))
        path = os.path.join('data', 'TestCaptures', 'testscreen.png')
        img.save(path)
    return img   
    
def ocr_int_from_subimage(sub_img, thres):
    # gray scale
    gray = sub_img.convert("L")

    # resize
    #new_size = (gray.width // 2, gray.height // 2)
    #big = gray.resize(new_size, Image.LANCZOS)

    # normalize based on threshold 
    bw = gray.point(lambda x: 0 if x < thres else 255, mode="1")

    # invert
    inv = ImageOps.invert(bw.convert("L")).convert("1")
    #inv.show()

    # OCR with single-line PSM and digit whitelist
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_EXE_PATH

    #config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    config = "--psm 13 -c tessedit_char_whitelist=0123456789"

    raw = pytesseract.image_to_string(inv, config=config).strip()

    # Return integer or None
    try:
        return int(raw)
    except ValueError:
        return None

def get_elixir(image):
    """check pixel color values which is the fastest way to get count of elixer"""
    bar_y = int(image.height * 0.9796)
    elixir_ratios = [
        0.3291,  # 1 elixir
        0.4051,  # 2
        0.4722,  # 3
        0.5424,  # 4
        0.6127,  # 5
        0.6797,  # 6
        0.7511,  # 7
        0.8228,  # 8
        0.8861,  # 9
        0.9536   # 10 elixir
    ]
    count = 0
    # loop through checking values
    for segment in elixir_ratios:
        pixel = image.getpixel((int(image.width * segment), bar_y))
        if (pixel[0] > 150):
            count += 1
        else: 
            break
    return count
    


def get_tower(image):
    """
    crops image to three specific spots, and runs OCR
    """
    # left tower
    w, h = image.size
    left   = int(w * 0.1983)
    top    = int(h * 0.1328)
    width  = int(w * 0.0715 * 1)
    height = int(h * 0.01896)

    left_sub = image.crop((left, top, left + width, top + height))

    # you can now save or work with sub_img
    left_sub.save("data/TestCaptures/leftTower.png")

    # right
    w, h = image.size
    left   = int(w * 0.7225)
    top    = int(h * 0.1328)
    width  = int(w * 0.0715 * 1.08)
    height = int(h * 0.01896)
    right_sub = image.crop((left, top, left + width, top + height))
 
    # you can now save or work with sub_img
    right_sub.save("data/TestCaptures/rightTower.png")

    # run OCR
    l_val = ocr_int_from_subimage(left_sub, 178)
    r_val = ocr_int_from_subimage(right_sub, 178)



    return l_val, r_val

def get_cards(image):
    """
    crops image to each of the 4 cards, runs template matching
    later update to work with more cards
    Currently works with: knight, archers, minions, arrows, fireball, giant, mini pecka, muskateer
    """
    cards = ["data/TestCaptures/card1.png", "data/TestCaptures/card2.png", 
             "data/TestCaptures/card3.png", "data/TestCaptures/card4.png"]

    # card 1
    w, h = image.size
    left   = int(w * 0.228)
    top    = int(h * 0.8331)
    width  = int(w * .17)
    height = int(h * .0958)

    card1 = image.crop((left, top, left + width, top + height))
    card1.save("data/TestCaptures/card1.png")

    # card 2
    left = int(w * 0.415)
    card2 = image.crop((left, top, left + width, top + height))
    card2.save("data/TestCaptures/card2.png")
    #print("left is", left)

    # card 3
    left = int(w * 0.6)
    card3 = image.crop((left, top, left + width, top + height))
    card3.save("data/TestCaptures/card3.png")
    #print("left is, ", left)

    # card 4
    left = int(w * 0.79)
    card4 = image.crop((left, top, left + width, top + height))
    card4.save("data/TestCaptures/card4.png")


    matched_cards = []

    for card in cards:

        # Load images
        card_img = Image.open(card).convert("L")
        full_array = np.array(card_img)

        max_match = -1
        matched_card = ""

        # iterates through templates in /Templates, later update to subfolder
        for filename in os.listdir("data/Templates"):
            template = Image.open("data/Templates/" + filename).convert("L")
            tempate_array = np.array(template)

            #Match template
            result = cv2.matchTemplate(full_array, tempate_array, cv2.TM_CCORR_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > max_match:
                max_match = max_val
                matched_card = filename

            #print(f"Match confidence is: {max_val:.3f} for template {filename} and image {card}")

        matched_cards.append(matched_card)

        #print(f"\ncard was identified as: {matched_card}\n")
        
    print(f"\n{matched_cards}\n")
