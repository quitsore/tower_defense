harvest = 0
for year in range(1, 13):
    print(f"year {year}")
    for field in range(1, 11):
        print(f"field {field} = {field**2}")
        harvest += field**2
print(f"{harvest} apples")
