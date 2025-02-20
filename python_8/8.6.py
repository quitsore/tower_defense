families = {"Einstein", "Cruiser", "Putin"}

while True:
    thing = input("What do you want to do? | ")

    if thing == "add":
        add = input("Add a family: ")
        if add in families:
            print("That family is already there")
        else:
            families.add(add)

    elif thing == "delete":
        delete = input("Delete a family: ")
        if delete not in families:
            print("That family doesn't exist")
        else:
            families.discard(delete)
    elif thing == "show families":
        print(families)
    elif thing == "exit":
        exit()