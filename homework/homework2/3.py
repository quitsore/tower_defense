import random
import time

options = ["stone", "stone", "gold"]
gold = 16
stone = 20
acquired_gold = 0
acquired_stone = 0

while acquired_gold < gold:
    if acquired_stone < stone:
        options_index = random.randint(0, 2)
    else:
        options_index = 2
    mining = options[options_index]
    match mining:
        case "stone":
            acquired_stone += 1
        case "gold":
            acquired_gold += 1
    print(f"acquired_gold: {acquired_gold}")
    print(f"acquired_stone: {acquired_stone}")
    time.sleep(1)
