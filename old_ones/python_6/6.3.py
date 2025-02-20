import random

choices = ["stone", "scissors", "paper"]
your_choice = ""
play = "y"
player_points = 0
bot_points = 0

while play == "y":
    your_choice = input("your choice: ")
    choice_index = choices.index(your_choice)
    bot = random.choice(choices)
    bot_index = choices.index(bot)
    print(bot)
    if choice_index == bot_index:
        print("tie")
    elif choice_index == 2 and bot_index == 0:
        print("you won")
        player_points += 1
    elif choice_index == 0 and bot_index == 1:
        print("you won")
        player_points += 1
    elif choice_index == 1 and bot_index == 2:
        print("you won")
        player_points += 1
    else:
        print("bot won")
        bot_points += 1
    play = input("play again? | ")
print(f"you: {player_points}")
print(f"bot: {bot_points}")
