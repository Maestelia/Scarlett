from skimage.metrics import structural_similarity as ssim
import cv2
import glob
import requests
import json
import sys
import os
from scryfall_DL import get_set

SCRYFALL_URL = "https://api.scryfall.com/cards/"


def best_match(img_in, folder):
    filelist = glob.glob(folder + "/*.jpeg")
    img_a = cv2.imread(img_in)
    best_score = 0
    best_id = ""
    for file in filelist:
        img_b = cv2.imread(file)
        img_b = cv2.resize(img_b, (img_a.shape[1], img_a.shape[0]))
        score = ssim(img_a, img_b, multichannel=True)
        if score > best_score:
            best_score = score
            best_id = file
    print(best_score)
    return best_id, best_score


def get_info(card_id):
    card_id = card_id.split('/')[-1][:-5]
    url = SCRYFALL_URL + card_id
    card_info = requests.get(url).json()
    return card_info["set_name"], card_info["name"]


if __name__ == '__main__':
    folder_in = sys.argv[1]
    exp = sys.argv[2]
    folder_cpr = "database/{}".format(exp.upper())
    if not os.path.isdir(folder_cpr):
        get_set(exp)
    files_in = glob.glob(folder_in + "/*.jpg")
    files_in = sorted(files_in)
    csv_out = open("PierreOdactyle.csv", "w")
    csv_out.write("Set,Card Name\n")
    print("{} cards to scan".format(str(len(files_in))))
    index = 0
    for img_in in files_in:
        best_id, best_score = best_match(img_in, folder_cpr)
        if best_score > 0.22:
            set_name, card_name = get_info(best_id)
            print("{} is {} ({})".format(img_in, card_name, set_name))
            csv_out.write("{},{}\n".format(set_name, card_name))
            os.remove(img_in)
        else:
            print("CANNOT IDENTIFY {}".format(img_in))
