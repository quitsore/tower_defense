print("You awoke in a little room without remembering about what happened. On the door is writen: "
      "Try to get out of here! You don't have much time left...")
choice = int(input("What will you do? | 1. Look at the door closer | 2. Look around | 3. Do nothing: "))

match choice:
    case 1:
        print("The door is closed")
        choice = int(input("What will you do? | 1. Look around | 2. Knock at the door | 3. Try to break out the door: "))

        match choice:
            case 1:
                print("You were sitting on a bed, in the room stands a locker. There is a window with a lock.")
                choice = int(input("What will you do? | 1. Look under the bed | 2. Open the locker | 3. Break out the window: "))

                match choice:
                    case 1:
                        print("You found a super key. You can open every lock with it.")
                        print("A bomb explodes in your chamber. You died.")

                    case 2:
                        print("The locker is locked")
                        print("A bomb explodes in your chamber. You died.")

                    case 3:
                        print("You heard an explosion. Everyone heard the noise of the window before. "
                              "Everyone chased you. You have nothing. You died")

            case 2:
                print("Someone opened the door. After that someone killed you. You died.")

            case 3:
                print("You broke out the door. There were a lot of people with weapons. You died.")

    case 2:
        print("You are sitting on a bed, in the room stands a locker. There is a window with a lock.")
        choice = int(input("What will you do? | 1. Look under the bed | 2. Open the locker | 3. Break out the window: "))
        match choice:
            case 1:
                print("You found a super key. You can open every lock with it")
                choice = int(input("What will you do? | 1. Open the door | 2. Open the locker | 3. Open the window: "))

                match choice:
                    case 1:
                        print("You opened the door. There were a lot of people with weapons. You died.")

                    case 2:
                        print("You opened the locker. There is a bomb. 3..2..1.. You died.")

                    case 3:
                        print("You opened and climbed through the window. You heard an explosion. "
                              "No one chased you. You escaped")

            case 2:
                print("You opened the locker. There is a bomb. 3..2..1.. You died.")

            case 3:
                print("You heard an explosion. Everyone heard the noise of the window before. "
                      "Everyone chased you. You have nothing. You died")

    case 3:
        print("You just do nothing. A minute later a bomb explodes in your chamber. You died.")
