sword = int(input("Sword available: "))
sword_broken = int(input("Sword broken: "))
shield = int(input("Shield available: "))

if sword and shield:
    print("Оба типа снаряжения присутствуют в инвентаре.")
    if sword_broken:
        print("Меч в инвентаре, но он сломан.")

else:
    print("Не все типы снаряжения присутствуют в инвентаре.")

if sword:
    print("В инвентаре есть только меч.")

elif shield:
    print("В инвентаре есть только щит.")

else:
    print("В инвентаре нет ни меча, ни щита.")