from django import template

register = template.Library()

@register.filter(name='get_range')
def get_range(value):
    return range(1, value + 1)

import random

@register.filter(name='random_color')
def random_color(value):
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))