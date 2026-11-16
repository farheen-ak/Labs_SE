def parse_declaration(text):
    if not isinstance(text, str):
        raise ValueError("Declaration must be a string")

    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("Expected category:value")

    category, value = parts
    category = category.strip()

    if not category:
        raise ValueError("Category cannot be empty")

    try:
        value = float(value.strip())
    except (ValueError, TypeError):
        raise ValueError("Value must be numeric")

    if value < 0:
        raise ValueError("Value cannot be negative")

    return category.lower(), value


def duty_amount(text):
    if not isinstance(text, str):
        raise ValueError("Duty input must be a string")

    parts = text.split("@")
    if len(parts) != 2:
        raise ValueError("Expected value@rate")

    try:
        value = float(parts[0].strip())
        rate = float(parts[1].strip())
    except (ValueError, TypeError):
        raise ValueError("Value and rate must be numeric")

    if value < 0 or rate < 0:
        raise ValueError("Value and rate cannot be negative")

    return value * rate / 100



def hs_chapter(code):
    if not isinstance(code, str):
        raise ValueError("HS code must be a string")

    code = code.strip()

    if not code:
        raise ValueError("HS code cannot be empty")

    parts = code.split(".")

    if len(parts) != 2:
        raise ValueError("Invalid HS code format")

    chapter = parts[0]
    suffix = parts[1]

    if len(chapter) < 2 or not chapter.isdigit():
        raise ValueError("Invalid HS chapter")

    if not suffix or not suffix.isdigit():
        raise ValueError("Invalid HS code suffix")

    return int(chapter[:2])


def main():
    print("==== Running parse_declaration ====")
    try:
        user_input = input("Enter category:value (e.g. electronics:25000): ")
        result = parse_declaration(user_input)
        print("Category and Value:", result)
    except ValueError as e:
        print("Invalid declaration:", e)

    print("\n==== Running duty_amount ====")
    try:
        user_input = input("Enter value@rate (e.g. 25000@20): ")
        result = duty_amount(user_input)
        print("Duty Amount:", result)
    except ValueError as e:
        print("Invalid duty input:", e)

    print("\n==== Running hs_chapter ====")
    try:
        user_input = input("Enter an HS code (e.g. 8517.12): ")
        result = hs_chapter(user_input)
        print("Chapter:", result)
    except ValueError as e:
        print("Invalid HS code:", e)


if __name__ == "__main__":
    main()
