from django import template

register = template.Library()


@register.filter(name='get_character_rating')
def get_character_rating(rating):
    if 1000 <= rating <= 9999:
        return f"{str(rating)[0]}.{str(rating)[1]}K"
    elif 10000 <= rating <= 99999:
        return f"{str(rating)[:2]}K"
    elif 100000 <= rating <= 999999:
        return f"{str(rating)[:3]}K"
    elif 99_999_999 >= rating >= 1_000_000:
        return f"{str(rating)[0]}.{str(rating)[1]}M"
    elif 999_999_999 >= rating >= 10_000_000:
        return f"{str(rating)[:2]}M"
    return f"{rating:.0f}"


@register.filter(name="get_character_gold")
def get_character_gold(gold):
    if gold == 1000:
        return f"{str(gold)[0]}K"
    if 1000 < gold <= 9999:
        return f"{str(gold)[0]}.{str(gold)[1]}K"
    elif 10000 <= gold <= 99999:
        return f"{str(gold)[:2]}K"
    elif 100000 <= gold <= 999999:
        return f"{str(gold)[:3]}K"
    elif 99_999_999 >= gold >= 1_000_000:
        return f"{str(gold)[0]}.{str(gold)[1]}M"
    elif 999_999_999 >= gold >= 10_000_000:
        return f"{str(gold)[:2]}M"
    return f"{gold:.0f}"


@register.filter(name='first_word')
def first_word(value):
    return '-'.join(value.lower().split(" ")) if value else ''
