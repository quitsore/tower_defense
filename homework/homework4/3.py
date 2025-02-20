original_text = """The game uses the sword as the main weapon. 
The sword has a high attack and can deal critical blows. 
The sword can also be improved by adding various enchantments.
Swords or not you decide"""
print(original_text)

original_weapon = "sword"
original_weapons = "swords"

original_up_name1 = original_weapon[0].upper() + original_weapon[1:]
original_up_name2 = original_weapons[0].upper() + original_weapons[1:]


new_weapon = input("what is the new name of the first one? | ")
new_weapons = new_weapon.__add__("s")

new_low_name1 = new_weapon.lower()
new_up_name1 = new_weapon[0].upper() + new_weapon[1:]

new_low_name2 = new_weapons.lower()
new_up_name2 = new_weapons[0].upper() + new_weapons[1:]

print(original_text.replace(original_weapon, new_low_name1).replace(original_up_name1, new_up_name1)
      .replace(original_weapons, new_low_name2).replace(original_up_name2, new_up_name2))
