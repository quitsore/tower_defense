from traceback import print_tb

chambers = int(input("How many chambers do you have? - "))

if chambers == 3:
    print("You have a three-room apartment")
elif chambers == 2:
    print("You have a two-room apartment")
elif chambers == 1:
    print("You have a studio apartment")
elif chambers == 0:
    print("You have a studio")
elif chambers > 3:
    print("You have a lot of rooms, cool!")
else:
    print("You can't have less than 0 chambers...")