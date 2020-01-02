from PIL import Image
import pytesseract
import cv2
import os
from fuzzywuzzy import fuzz, process
from names_example import all_names


def get_text(input_image):
    image = cv2.imread(input_image)
    # Rescale the image TODO
    image = cv2.resize(image, None, fx=1.5, fy=1.5,
            interpolation=cv2.INTER_CUBIC)
    # Convert to gray
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # TODO more
    # write the grayscale image to disk as a temporary file so we can apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    # load the image as a PIL/Pillow image, apply OCR, whitelist to
    # chars upper and lowercase and then delete the temporary file
    # TODO not sure the whitelist works
    whitelist = "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    text = pytesseract.image_to_string(Image.open(filename), config = whitelist)
    os.remove(filename)
    text = clean_text(text)
    return text

def clean_text(text):
    # make list of addresses
    text = text.split("\n")
    name_text = ""
    for line in text:
        if fuzz.token_set_ratio("2019", line) > 75 or fuzz.token_set_ratio("42 silicon valley", line) > 75:
            pass
        elif line.strip():
            print(line)
            dc = fuzz.token_set_ratio("6600 Dumbarton Circle", line)
            ac = fuzz.token_set_ratio("Ardentech Court", line)
            fm = fuzz.token_set_ratio("94555 Freemont", line)
            print("dc", dc)
            print("ac", ac)
            print("fm", fm)
            if dc > 75 or ac > 75 or fm > 75:
                break
            name_text += " " + line
    return name_text

def get_names(text):
    # use fuzzy search to get a selection of the possible names
    users = process.extract(text, all_names, scorer=fuzz.token_set_ratio, limit=3)
    return (users)


def start():
    # get text from image
    text = get_text("current.jpg")
    while text == "":
        return ("no_text")
    print("READ TEXT: \n", '\033[35m', text, '\033[0m')
    options = get_names(text)
    return options

