import random

print("""Let's play cities! I make a wish for the city
you must name the city whose name begins
from the last letter of my city.""")
score = 0
cities = ["Bryansk", "Kaliningrad", "Moscow", "St. Petersburg", "Yekaterinburg", "Novosibirsk", "Kazan", "Chelyabinsk",
          "Omsk", "Samara", "Amsterdam", "Berlin", "Zurich", "Paris", "Geneve", "New York", "Hong Kong"]

while cities:
    city = random.choice(cities)
    print(f"My city is {city}")
    last_letter = city[-1].lower()
    user_city = input("Enter city: ").strip()
    if user_city[0].lower() == last_letter:
        print("fine")
        score += 1
        cities.remove(city)
        if user_city in cities:
            cities.remove(user_city)

    else:
        print(f"Nope, the last letter is {last_letter}")
        break

print(f"You won {score} points")
