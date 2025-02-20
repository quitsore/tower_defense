multipliers = int(input("How many multipliers: "))
total = 1

for i in range(multipliers):
    print(f"{total}*{i+1} = {total * (i+1)}")
    total *= (i+1)

print(f"the total is {total}")