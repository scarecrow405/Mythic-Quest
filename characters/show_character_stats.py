# Calculate stats of character and put the appropriate values in the context
def get_character_stat(character_stat):
    if 9_999 >= character_stat >= 1_000:
        return f"{str(character_stat)[0]}.{str(character_stat)[1]}K"
    elif 99_999 >= character_stat >= 10_000:
        return f"{str(character_stat)[:2]}K"
    elif 999_999 >= character_stat >= 100_000:
        return f"{str(character_stat)[:3]}K"
    elif 99_999_999 >= character_stat >= 1_000_000:
        return f"{str(character_stat)[0]}.{str(character_stat)[1]}M"
    elif 999_999_999 >= character_stat >= 10_000_000:
        return f"{str(character_stat)[:2]}M"
    return character_stat
