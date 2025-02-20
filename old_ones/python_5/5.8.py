km = 10
day = 1
print(km)
print(day)

while  km < 200:
    km *= 1.1
    day += 1
    print(day)
    print(km)
    print()
print(f"После {day} дней суммарный пробег лыжника превысит 200 км и составит {km:.2f} км.")