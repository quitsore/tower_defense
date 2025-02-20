word = "diamond"
a = len(word)
b = a//2
if a % 2 != 0:
     b += 1
print(word[0:b])
print(word[b:a])
