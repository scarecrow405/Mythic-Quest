from django import template

register = template.Library()


@register.filter(name='get_character_rating')
def get_character_rating(rating):
    if 1000 <= rating <= 9999:
        return f"{str(rating)[0]}.{str(rating)[1]}K"
    elif 10000 <= rating <= 99999:
        return f"{str(rating)[0]}.{str(rating)[1]}K"
    elif 100000 <= rating <= 999999:
        return f"{str(rating)[0]}.{str(rating)[1]}K"
    return f"{rating:.0f}"


@register.filter(name='first_word')
def first_word(value):
    return '-'.join(value.lower().split(" ")) if value else ''
