a = 1
b = 2
c = 3

armor = a
helmet = b

if armor == helmet:
    print("Предметы экипировки совместимы.")
else:
    print("Предметы экипировки несовместимы.")

armor_broken = True
helmet_broken = False

if armor == helmet and armor_broken == True or helmet_broken == True:
    print("Предметы экипировки совместимы, но один из них сломан.")
elif armor != helmet and armor_broken == False and helmet_broken == False:
    print("Предметы экипировки несовместимы, но оба целы.")
elif armor != helmet and armor_broken == True or helmet_broken == True:
    print("Предметы экипировки несовместимы и один из них сломан.")
elif armor == helmet and armor_broken == False and helmet_broken == False:
    print("Предметы экипировки совместимы и оба целы.")
