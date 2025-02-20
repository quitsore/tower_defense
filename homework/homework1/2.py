score = int(input("Your score: "))
min_score = int(input("Needed score: "))

if score >= min_score:
    print("Игрок набрал достаточное количество очков для прохождения уровня.")
else:
    print("Игрок не набрал достаточное количество очков для прохождения уровня.")

if score > min_score * 2:
    print("Игрок набрал в два раза больше очков, чем необходимо.")
elif score == min_score:
    print("Игрок набрал ровно необходимое количество очков.")
elif min_score / 2 > score >= 10:
    print("Игрок набрал менее половины необходимых очков.")
elif score < 10:
    print("Игрок набрал очень мало очков.")