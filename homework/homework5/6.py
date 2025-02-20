cubes = int(input("How many cubes: "))
total = 1

for i in range(cubes):
    print(f"{total}+{(i+1)**3} = {total + ((i+1)**3)}")
    total += (i+1)**3

print(f"the total is {total}")
