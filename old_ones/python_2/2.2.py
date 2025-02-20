colors = input("What does mean this color for you? - ")

match colors:
    case "Red":
        print("Strawberry")
    case "Green" | "Brown" | "Diamonds":
        print("Nature")
    case "Blue":
        print("Just water")
    case _:
        print("Nope")