word = input("Your word is: ")

match word:
    case "run" | "write" | "read" | "eat" | "play" | "work":
        print("Verb")
    case "Tree" | "Mouse" | "Toy" | "Computer" | "Backpack" | "Apple":
        print("noun")
    case "big" | "strong" | "small" | "mad" | "happy" | "smart":
        print("adjective")
