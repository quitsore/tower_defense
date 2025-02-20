running = True
listo = [1,7,3,9,4,8,4,7,3,0,8,9,6,4,5,8,9,5,2,6,8,0,6,4,3,6,8,3,7,0,5,3,4,7,9,4,1,4,7,9,6,4,3,2]
print(listo)

while running:
    activity = input("What do you want to do? | ")

    if activity == "delete":
        listo.pop(-1)
        print(listo)
    elif activity == "count":
        counting = int(input("What do you want to count? | "))
        x = listo.count(counting)
        print(x)
    elif activity == "stop":
        running = False
    else:
        print("No command like this")
