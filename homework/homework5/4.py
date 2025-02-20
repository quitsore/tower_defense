import random
from typing import Dict, List

choices = ["stone", "scissors", "paper", "crayon", "fire", "water", "bottle of lemonade", "iron wall"]
your_choice = ""
play = "y"
your_score = 0
bots_score = 0

win_list : Dict[str, List[str]] = {"stone": ["scissors", "fire"],
                                   "scissors": ["paper", "crayon"],
                                   "paper": ["stone", "water", "bottle of lemonade", "iron wall"],
                                   "crayon": ["stone", "paper"],
                                   "fire": ["scissors", "paper", "crayon"],
                                   "water": ["stone", "scissors", "paper", "iron wall"],
                                   "bottle of lemonade": ["stone", "scissors", "crayon", "fire", "iron wall"],
                                   "iron wall": ["stone", "scissors", "crayon", "fire"]}
print(choices)
while play == "y":
    your_choice = input("your choice: ")
    bot_choice = random.choice(choices)
    print(f"bot's choice: {bot_choice}")
    if win_list.get(your_choice) is None:
        print("wrong input")
        continue
    elif your_choice == bot_choice:
        print("tie")
    elif win_list[your_choice].count(bot_choice) > 0:
        print("you won")
        your_score += 1
    elif win_list[bot_choice].count(your_choice) > 0:
        print("bot won")
        bots_score += 1
    else:
        print("something got wrong")
    play = input("play again? (y/n) | ")
print(f"Your score is {your_score}")
print(f"Bot's score is {bots_score}")
