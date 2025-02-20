amount = 0
football = 1500
basket_ball = 1200
volley_ball = 1000
tennis_racket = 2500
sneakers = 3000
sports_bag = 1800
items = [football, basket_ball, volley_ball, tennis_racket, sneakers, sports_bag]
plus = 0
for i in range(len(items)):
    plus = items[i]
    amount += plus
print(amount)
