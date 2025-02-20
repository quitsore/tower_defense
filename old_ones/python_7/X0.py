XO = [[" ", " ", " "],
      [" ", " ", " "],
      [" ", " ", " "]]
print("-------------")
for i in range(3):
    row = "| "
    for j in range(3):
        row += XO[i][j] + " | "
    print(row)
    print("-------------")

player = "X"
count = 0
win = False

while (not win) and (count != 9):
    print("player", player, "Your turn")
    row = int(input("Enter row number (0-2): "))
    if 0 <= row < 3:
        col = int(input("Enter column number (0-2): "))
        if 0 <= col < 3:
            if XO[row][col] == " ":
                XO[row][col] = player
                count += 1
                print("-------------")
                for i in range(3):
                    row = "| "
                    for j in range(3):
                        row += XO[i][j] + " | "
                    print(row)
                    print("-------------")
                for i in range(3):
                    if XO[i][0] == player and XO[i][1] == player and XO[i][2] == player:
                        print(f"player {player} won")
                        win = True
                        break
                    if XO[0][i] == player and XO[1][i] == player and XO[2][i] == player:
                        print(f"player {player} won")
                        win = True
                        break
                if XO[0][0] == player and XO[1][1] == player and XO[2][2] == player:
                    print(f"player {player} won")
                    win = True
                    break
                if XO[2][0] == player and XO[1][1] == player and XO[0][2] == player:
                    print(f"player {player} won")
                    win = True
                    break
                if player == "X":
                    player = "O"
                else:
                    player = "X"
            else:
                print("place filled, try again")
        else:
            print("wrong input, try again")
    else:
        print("wrong input, try again")
    print()
if not win:
    print("tie")