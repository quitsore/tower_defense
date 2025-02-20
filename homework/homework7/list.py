running = True
listo = [1,7,3,9,4,8,4,7,3,0,8,9,6,4,5,8,9,5,2,6,8,0,6,4,3,6,8,3,7,0,5,3,4,7,9,4,1,4,7,9,6,4,3,2]
print(listo)
print("Commands:\nadd\ndelete last element\ndelete by value\ndelete by index\ncount\nshow list\nclear",
      "\nshow greatest number\nminimalize greatest number\nmultiply in list\nexit\n")

while running:
    activity = input("What do you want to do? | ")

    if activity == "add":
        adding = int(input("What do you want to add? | "))
        listo.append(adding)
        print(f"{adding} added to list")

    elif activity == "delete last element":
        listo.pop(-1)
        print("last element deleted")

    elif activity == "delete by value":
        delete = int(input("What do you want to delete? | "))

        if delete not in listo:
            print("number in list not found")

        else:
            y = listo.count(delete)
            for i in range(y):
                listo.remove(delete)
            print(f"every {delete} was deleted from list")

    elif activity == "delete by index":
        delete_index = int(input("What index do you want to delete? | "))

        if delete_index > len(listo):
            print("index not found")

        else:
            listo.pop(delete_index)
            print(f"index {delete_index} was deleted")

    elif activity == "count":
        counting = int(input("What do you want to count? | "))

        if counting not in listo:
            print("number in list not found")

        else:
            x = listo.count(counting)
            print(f"the number {counting} was {x} times found")

    elif activity == "show list":
        print(listo)

    elif activity == "clear":
        listo.clear()
        print("list cleared")

    elif activity == "show greatest number":
        max_num = 0
        for i in listo:
            if i > max_num:
                max_num = i
        print(max_num)

    elif activity == "minimalize greatest number":
        great_num = 0
        for i in listo:
            if i > great_num:
                great_num = i
        for i in range(len(listo)):
            if listo[i] == great_num:
                listo[i] = 0
        print("the greatest number is now 0")

    elif activity == "multiply in list":
        total = 1
        for i in listo:
            total *= i
        print(f"the total of multiplying every number in list is {total}")

    elif activity == "exit":
        running = False
    else:
        print("no command like this")
