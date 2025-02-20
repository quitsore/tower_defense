original_text = """Mario: Hello, Luigi! How are you?
Luigi: Hi, Mario! I'm fine, how are you?
Mario: I'm fine too. Let's go on an adventure!"""

print(original_text)

original_low_name1 = "mario"
original_low_name2 = "luigi"

original_up_name1 = original_low_name1[0].upper() + original_low_name1[1:]
original_up_name2 = original_low_name2[0].upper() + original_low_name2[1:]


new_name1 = input("what is the new name of the first one? | ")
new_name2 = input("what is the new name of the second one? | ")

new_low_name1 = new_name1.lower()
new_up_name1 = new_name1[0].upper() + new_name1[1:]

new_low_name2 = new_name2.lower()
new_up_name2 = new_name2[0].upper() + new_name2[1:]

print(original_text.replace(original_low_name1, new_low_name1).replace(original_up_name1, new_up_name1)
      .replace(original_low_name2, new_low_name2).replace(original_up_name2, new_up_name2))
