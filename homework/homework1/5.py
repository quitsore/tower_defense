speed = int(input("Your speed: "))
min_speed = 80
max_speed = 120

if max_speed >= speed >= min_speed:
    print("Скорость находится в допустимом диапазоне.")
else:
    print("Скорость выходит за пределы допустимого диапазона.")

if speed < min_speed:
    print("Скорость слишком низкая.")
elif speed > max_speed:
    print("Скорость слишком высокая.")
elif speed == min_speed:
    print("Скорость на минимальном уровне.")
elif speed == max_speed:
    print("Скорость на максимальном уровне.")
else:
    print("Скорость в середине допустимого диапазона.")