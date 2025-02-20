import random

print("""Let's play fruits! I make a wish for the fruit
you must name the fruit whose name begins
from the last letter of my fruit.""")
score = 0
fruits = ["Apple", "Banana", "Pear", "Mango", "Kiwi", "Orange", "Mandarin", "Ananas", "Lemon", "Grapefruit",
          "Melon"]

while fruits:
    fruit = random.choice(fruits)
    print(f"My fruit is {fruit}")
    first_letter = fruit[0].lower()
    user_fruit = input("Enter fruit: ").strip()
    if user_fruit[0].lower() == first_letter:
        print("fine")
        score += 1
        fruits.remove(fruit)
        if user_fruit in fruits:
            fruits.remove(user_fruit)

    else:
        print(f"Nope, the first letter is {first_letter}")
        break

print(f"You won {score} points")
