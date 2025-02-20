original_text = """The Legend of Zelda — это игра,
которая покорила сердца миллионов игроков!
Погрузитесь в волшебный мир the legend of zelda и станьте частью легенды.
THE LEGEND OF ZELDA ждет вас!"""

original_game = "The Legend of Zelda"

print(original_text)

new_game = input("what is your new game's name? | ")

lower_case_original_text = original_text.lower()
lower_case_original_game = original_game.lower()

text = original_text
orig_pos = 0
while orig_pos != -1:
    orig_pos = lower_case_original_text.find(lower_case_original_game, orig_pos)
    if orig_pos != -1:
        text = text[0:orig_pos] + lower_case_original_game + text[orig_pos + len(original_game):]
        orig_pos += len(original_game)

print(text.replace(lower_case_original_game, new_game))