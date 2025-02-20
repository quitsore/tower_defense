a = int(input())
b = 200
total = 0

if a > b:
    exit()

for num in range(b - a + 1):
    print(f"{total} + {a} = {total + a}")
    total += a
    a += 1
    if a == b + 1:
        total = total / (num + 1)
print(total)