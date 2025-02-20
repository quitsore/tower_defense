import math

number = int(input("your number: "))

is_prime = True
for x in range(2, int(math.sqrt(number)) + 1):
    if number % x == 0:
        is_prime = False
        break

if is_prime:
    print("your number is a prime number")

else:
    print("your number is not a prime number")