num = int(input())
end_num = int(input())

while num != end_num:
    if num % 2 == 0:
        print(":2")
        num = num / 2
    else:
        print("-1")
        num = num - 1
    print(num)
