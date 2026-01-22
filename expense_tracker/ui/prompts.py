def prompt(text: str, required: bool = True):
    while True:
        value = input(f"{text}: ").strip()
        if value or not required:
            return value
        print("❌ This field is required.")


def prompt_choice(text: str, choices: list):
    choices_str = "/".join(choices)
    while True:
        value = input(f"{text} ({choices_str}): ").strip().lower()
        if value in choices:
            return value
        print(f"❌ Choose one of {choices_str}")
