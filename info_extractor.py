# extract all the necessary information on a given game state (image)

#### IMPORTS ####
import os
from PIL import Image, ImageOps
import pytesseract
import cv2
import numpy as np

def extract():
    """Puts together information extracted by OCR in the game"""

    # get image from folder

    dir = os.path.join(os.path.dirname(__file__) , "data/TestCaptures")
    image_path = os.path.join(dir, "testscreen.png")
    image = Image.open(image_path)

    print(image.size)

    # time left in seconds
    #time_remaining = get_time(image) # or set a timer
    
    # Enemy tower information
    l, r = get_tower(image)
    print(f"Left Tower health: {l}")
    print(f"Right Tower health: {r}")


    # Cards on screen, oponent/user (OCR)


    # User tower information

    # get elixir (optional)

    #e = get_elixir()

    # Cards in hand w/their information

    # return
    return l, r

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
    #new_size = (gray.width * 4, gray.height * 4)
    #big = gray.resize(new_size, Image.LANCZOS)

    # normalize based on threshold 150
    bw = gray.point(lambda x: 0 if x < thres else 255, mode="1")

    # invert
    inv = ImageOps.invert(bw.convert("L")).convert("1")
    # inv.show()

    # OCR with single-line PSM and digit whitelist
    # comment this out if its not on windows
    if os.getlogin() == 'mfouc':
        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\mfouc\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
    else:
        pytesseract.pytesseract.tesseract_cmd = r"D:\Program Files\tesseract.exe"

    config = "--psm 7 -c tessedit_char_whitelist=0123456789"
    raw = pytesseract.image_to_string(inv, config=config).strip()

    # Return integer or None
    try:
        return int(raw)
    except ValueError:
        return None

def get_elixir():
    """get a cropped image of the elixir with open CV template matching"""

    # Load images
    full_img = Image.open("data/TestCaptures/testscreen.png").convert("L")
    template = Image.open("data/template.png").convert("L")

    full_array = np.array(full_img)
    tempate_array = np.array(template)

    # Match template
    result = cv2.matchTemplate(full_array, tempate_array, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"Match confidence: {max_val:.3f} at {max_loc}")

    x, y = max_loc

    # Offset to where number is expected
    offset_x = 90
    offset_y = 0
    box_width = 80
    box_height = 75

    # Crop number region
    number_box = (x + offset_x, y + offset_y, x + offset_x + box_width, y + offset_y + box_height)
    sub_img = Image.open("data/TestCaptures/testscreen.png").crop(number_box)

    # run OCR
    print(ocr_int_from_subimage(sub_img, 190))


def get_tower(image):
    """
    crops image to three specific spots, and runs OCR
    """
    # left tower
    w, h = image.size
    left   = int(w * 0.1983)
    top    = int(h * 0.1328)
    width  = int(w * 0.0717 * 1.18)
    height = int(h * 0.01896)

    left_sub = image.crop((left, top, left + width, top + height))

    # you can now save or work with sub_img
    left_sub.save("data/TestCaptures/leftTower.png")

    # right
    w, h = image.size
    left   = int(w * 0.7253)
    top    = int(h * 0.1328)
    width  = int(w * 0.0717 * 1.18)
    height = int(h * 0.01896)
    right_sub = image.crop((left, top, left + width, top + height))

    # you can now save or work with sub_img
    right_sub.save("data/TestCaptures/rightTower.png")

    # run OCR
    l_val = ocr_int_from_subimage(left_sub, 180)
    r_val = ocr_int_from_subimage(right_sub, 180)
    return l_val, r_val

extract()