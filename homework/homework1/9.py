experience = int(input("Your experience: "))
level_up_experience = int(input("Needed score: "))

if experience >= level_up_experience:
    print("Персонаж получил достаточно опыта для повышения уровня.")
else:
    print("Персонаж не получил достаточно опыта для повышения уровня.")

if experience > level_up_experience * 2:
    print("Персонаж получил в два раза больше опыта, чем необходимо для повышения уровня.")
elif experience == level_up_experience:
    print("Персонаж получил ровно необходимое количество опыта для повышения уровня.")
elif level_up_experience / 2 > experience >= 10:
    print("Персонаж получил менее половины необходимого опыта.")
elif experience < 10:
    print("Персонаж получил очень мало опыта.")
