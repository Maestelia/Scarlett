import json
import requests
import os
import sys
import time


def get_images(cards, dest):
    try:
        os.mkdir(dest)
    except OSError:
        pass

    index = 0
    for card in cards:
        scryfall_id, uri = card
        img = requests.get(uri).content
        with open(dest + scryfall_id + ".jpeg", "wb") as f:
            f.write(img)
        index += 1
        if index % 10 == 0:
            print("{} cards downloaded".format(str(index)))
        time.sleep(0.1)


def get_cards(card_file, exp):
    cards = []
    with open(card_file, "r") as f:
        all_cards = json.load(f)
    for card in all_cards:
        if card["set"] == exp:
            cards.append((card["id"], card["image_uris"]["normal"]))
    return cards


if __name__ == '__main__':
    card_file = "utils/default-cards-20211113100239.json"
    exp = sys.argv[1]
    dest_folder = exp.upper() + "/"
    cards = get_cards(card_file, exp)
    print("Starting download for {}, {} cards to be downloaded".format(exp.upper(), str(len(cards))))
    get_images(cards, dest_folder)
