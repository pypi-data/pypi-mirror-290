def choice(options: list[str], prompt: str = "Please enter an option: ", failMsg: str = "\n", keyboardInterruptMsg: str = "keyboard interrupted", eofMessage: str = "EOF", caseSensitive: bool = False) -> str:
    temp = ""
    if not caseSensitive:
        choices = [item.lower() for item in options]
    while temp not in choices:
        print(prompt)
        try:
            temp = input(prompt)
            if not caseSensitive:
                temp = temp.lower()
        except EOFError:
            continue
        except KeyboardInterrupt:
            print(keyboardInterruptMsg)
            exit()
        print(failMsg)