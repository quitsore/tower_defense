matrix = ([1, 2, 3, 4],
          [5, 6],
          [7, 8, 9])

print(matrix[1][1])
print()

for i in range(len(matrix)):
    for j in range(len(matrix[i])):
        print(matrix[i][j], end=" ")
    print()
