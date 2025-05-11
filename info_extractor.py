# extract all the necessary information on a given game state (image)

#### IMPORTS ####
import os
from PIL import Image, ImageOps
import pytesseract


def extract():
    """Puts together information extracted by OCR in the game"""

    # get image from folder

    dir = os.path.join(os.path.dirname(__file__) , "data/TestCaptures")
    image_path = os.path.join(dir, "testscreen.png")
    image = Image.open(image_path)

    print(image.size)
    image = updateImageSize(image)
    print(image.size)

    # time left in seconds
    #time_remaining = get_time(image) # or set a timer
    
    # Enemy tower information
    l, r = get_tower(image)
    print(f"Left Tower health: {l}")
    print(f"Right Tower health: {r}")
    # Cards on screen, oponent/user

    # User tower information

    # Cards in hand w/their information

def updateImageSize(img):
    width, height = img.size
    if width != 614 or height != 1094:
        img = img.resize((614, 1094), Image.LANCZOS)
        #img = img.crop((0, 30, img.width - 30, img.height))
        path = os.path.join('data', 'TestCaptures', 'testscreen.png')
        img.save(path)
    return img   
    


def ocr_int_from_subimage(sub_img):
    # gray scale
    gray = sub_img.convert("L")

    # resize
    #new_size = (gray.width * 4, gray.height * 4)
    #big = gray.resize(new_size, Image.NEAREST)

    # normalize based on threshold 150
    bw = gray.point(lambda x: 255 if x > 180 else 0, mode="1")

    # invert
    inv = ImageOps.invert(bw)
    inv.show()

    # OCR with single-line PSM and digit whitelist
    config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    raw = pytesseract.image_to_string(inv, config=config).strip()

    # Return integer or None
    try:
        return int(raw)
    except ValueError:
        return None

def get_time(image):
    """get Image from top right, uses OCR for the time in seconds"""

    # Extract Top Right

    # Run OCR
    time_string = pytesseract.image_to_string(image)
    minutes, seconds = map(int, time_string.split(":"))

    return minutes * 60 + seconds

def get_tower(image):
    """
    crops image to three specific spots, and runs OCR
    """
    # left
    left, top = 72, 88
    width, height = 30, 12

    crop_box = (left, top, left + width, top + height)
    left_sub = image.crop(crop_box)

    # you can now save or work with sub_img
    left_sub.save("data/TestCaptures/leftTower.png")

    # right
    left, top = 265, 88
    width, height = 30, 12

    crop_box = (left, top, left + width, top + height)
    right_sub = image.crop(crop_box)

    # you can now save or work with sub_img
    right_sub.save("data/TestCaptures/rightTower.png")

    # run OCR
    l_val = ocr_int_from_subimage(left_sub)
    r_val = ocr_int_from_subimage(right_sub)
    return l_val, r_val


extract()