month = int(input("Which month is now? - "))

if month == 12 or month == 1 or month == 2:
    print("winter")
elif 3 <= month <= 5:
    print("spring")
elif 6 <= month <= 8:
    print("summer")
elif 9 <= month <= 11:
    print("autumn")
else:
    print("?")
