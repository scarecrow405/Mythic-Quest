from django import template

register = template.Library()


@register.filter(name='first_word')
def first_word(value):
    return value.split(" ")[0] if value else ''
