import random

winning_number = int(input("The winning_number is (from 1 to 10): "))
ticket_number = random.randint(1, 10)
print(f"Your ticket number is {ticket_number}")

if ticket_number == winning_number:
    print("Поздравляем! Вы выиграли в лотерею!")

else:
    print("К сожалению, вы не выиграли.")


if ticket_number == winning_number - 1 or ticket_number == winning_number + 1:
    print("Вы были очень близки к выигрышу!")
elif ticket_number == winning_number - 2 or ticket_number == winning_number + 2:
    print("Вы были близки к выигрышу.")
elif ticket_number == winning_number - 3 or ticket_number == winning_number + 3:
    print("Вы были недалеко от выигрыша.")
elif ticket_number == winning_number - 4 or ticket_number == winning_number + 4:
    print("Вы были далеки от выигрыша.")
elif ticket_number == winning_number - 5 or ticket_number == winning_number + 5:
    print("Вы были очень далеки от выигрыша.")
