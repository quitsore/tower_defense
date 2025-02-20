health = 20
damage = int(input("enter damage: "))
health -= damage

if health > 20:
    print("Thank's for health buff")

elif health > 5:
    print("you survived")

elif health > 0:
    print("you almost died")

elif health > -10:
    print("you're dead")

else:
    print("That's a lot of damage")