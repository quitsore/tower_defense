year = int(input("Your year: "))

if year % 4 == 0 and year % 100 != 0:
    print("yes")
else:
    print("no")
