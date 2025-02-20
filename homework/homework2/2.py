import random

choices = ["stone", "scissors", "paper"]

comp_index = random.randint(0,2)
choice = input("your choice: ")
try:
    choice_index = choices.index(choice)
    print(f"Comp's choice: {choices[comp_index]}")
    difference = (comp_index - choice_index) % 3
    match difference:
        case 0:
            print("tie")
        case 1:
            print("you won")
        case 2:
            print("you lost")
except:
    print("wrong input. game over.")
