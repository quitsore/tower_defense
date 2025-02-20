import time
import random

a = random.randint(20, 50)
b = random.randint(30, 60)

print("You are walking in the park. Suddenly you see your best friend going somewhere")
time.sleep(6)
print("Friend: Hey, hello")
time.sleep(1)
print("You: Hi, how are you?")
time.sleep(1.5)
print("Friend: I'm fine and you?")
time.sleep(1.5)
print("You: also")
time.sleep(1)
print("Friend: You know what, I'm going tomorrow to a theater")
time.sleep(3)
print("You: Sounds nice")
time.sleep(1.5)
print("Friend: Yeah, but my brother wants to come with me and I have not enough money for him, so I was curious "
      "if you can borrow me some?")
time.sleep(8)
print(f"You: Yeah sure. Are {a} dollars enough?")
time.sleep(2)

if a >= b:
    print("Friend: Yes, that's enough, thanks")
    time.sleep(1.5)
    print("You: you're welcome")
else:
    print(f"Friend: No... I need like {b-a} more")
    time.sleep(2)
    print("You: Ok, here you go")
    time.sleep(1)
    print("Friend: Thanks")
