import random
import time

rounds = int(input("rounds to play: "))
round = 1

wins1 = 0
wins2 = 0

player1 = input("Name first character: ")
player2 = input("Name second character: ")

while rounds > 0:
    print(f"round {round}")
    round += 1
    throw1 = random.randint(1, 6)
    throw2 = random.randint(1, 6)

    print(f"{player1} выбросил: {throw1}")
    print(f"{player2} выбросил: {throw2}")

    if throw1 > throw2:
        print(f"{player1} победил!")
        wins1 += 1

    elif throw2 > throw1:
        print(f"{player2} победил!")
        wins2 += 1

    else:
        print("ничья")

    rounds -= 1
    time.sleep(2)

if wins1 > wins2:
    print(f"{player1} победил в большинстве игр!")
    wins1 += 1

elif wins2 > wins1:
    print(f"{player2} победил в большинстве игр!")
    wins2 += 1

else:
    print("ничья")
