# Usage:
# Run from the command line
# $ python3 UmlConvert.py
#
# Copy and paste a C# method declaration and receive it back in UML format
# E.g. "static private Map<T> Do(T thing)" yields "- Do(thing : T) : Map<T>"
#
# It's pretty tolerant of whitespace and other junk like semicolons but it's not 100% perfect

import sys

modifierMap = {
    "private protected": "#",
    "protected internal": "+",
    "private": "-",
    "internal": "#",
    "protected": "#",
    "public": "+"
}

print("CTRL-C then ENTER to exit.")

while True:
    try:
        inString = str(input("Input method declaration: ")).strip()

        # Deduce return type and method name
        endIndex = inString.find("(")
        nameFlag = False
        openAngleBracketCount = 0
        for i in range(endIndex, -1, -1):
            if inString[i] == ">":
                openAngleBracketCount = openAngleBracketCount + 1
                continue
            if inString[i] == "<":
                openAngleBracketCount = openAngleBracketCount - 1
                continue

            if (inString[i] == " " or i == 0) and openAngleBracketCount == 0:
                if not nameFlag:
                    umlMethodName = inString[i:endIndex].strip()
                    nameStartIndex = i
                    nameFlag = True
                else:
                    returnTypeStartIndex = i
                    umlReturnType = inString[i:nameStartIndex].strip()
                    break

        # Turn the arguments into UML form
        args = inString[inString.find("(") + 1: inString.rfind(")")]
        umlArgs = ""
        for arg in args.split(","):
            if arg == "":
                break
            arg = arg.strip()
            arg = arg.replace(" ", "", arg.count(" ") - 1)  # remove all spaces but one separating the name and the type
            words = arg.split(" ")
            umlArgs = umlArgs + f"{words[1]} : {words[0]}, "
        umlArgs = umlArgs[0:len(umlArgs) - 2]

        # Determine access modifier
        umlModifier = "#"
        modifierString = inString[0:returnTypeStartIndex]
        for modifier in modifierMap:
            if modifierString.find(modifier) != -1:
                umlModifier = modifierMap[modifier]
                break

        # Done
        print(f"{umlModifier} {umlMethodName}({umlArgs}) : {umlReturnType}")

    except KeyboardInterrupt:
        sys.exit()
    except Exception:
        print("Error. Please ensure the input was formatted correctly.")
