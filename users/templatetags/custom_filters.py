from django import template




register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



@register.filter
def add(value, arg):
    if value is None or arg is None:
        return 1
    return value + arg