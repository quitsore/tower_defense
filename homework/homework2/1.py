import random

rand_num = random.randint(1, 100)

your_number = int(input("Guess the number: "))
attempts = 1

while your_number != rand_num:
    if your_number < rand_num:
        print("the number is bigger")

    else:
        print("the number is smaller")

    your_number = int(input("Guess the number: "))
    attempts += 1

print(f"you guessed {rand_num} right in {attempts} attempts, congrats")
