original_text = """Your quest begins in the forest.
The forest is full of dangers and mysteries.
Your task is to find an ancient artifact hidden in the forest.
The forest is guarded by powerful creatures. Forest"""
print(original_text)

original_weapon = "forest"

original_up_name = original_weapon[0].upper() + original_weapon[1:]


new_weapon = input("what is the new name of the first one? | ")

new_low_name = new_weapon.lower()
new_up_name = new_weapon[0].upper() + new_weapon[1:]


print(original_text.replace(original_weapon, new_low_name).replace(original_up_name, new_up_name))
