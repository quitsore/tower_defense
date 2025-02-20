import random
import time

points = 0


def test_subject(subject: str, question: str, answer) -> int:
    ok = 0
    print(subject)
    time.sleep(1)
    print(question)
    time.sleep(0.5)
    choice = type(answer)(input("What is your answer? | "))
    if choice == answer:
        print("You're right")
        ok = 1
    else:
        print(f"No, the answer is {answer}")
    return ok


def math() -> int:
    ok = 0
    print("Math")
    time.sleep(1)
    question = "What does %s + %s make?"
    num1 = random.randint(1, 100)
    num2 = random.randint(1, 100)
    print(question % (num1, num2))
    answer = num1 + num2
    time.sleep(0.5)
    choice = int(input("What is your answer? | "))
    if choice == answer:
        print("You're right")
        ok = 1
    else:
        print(f"No, the answer is {answer}")
    return ok

print("We are starting with school.")
time.sleep(1)
points += test_subject(subject="Geography", question="Which country is the greatest?", answer="Russia")
time.sleep(1)
points += math()
time.sleep(1)
points += test_subject(subject="History", question="When was the big French revolution?", answer=1789)
time.sleep(1)
points += test_subject(subject="Biology", question="How many legs does spiders have?", answer=8)
print(f"You did {points} of 4 questions right")
