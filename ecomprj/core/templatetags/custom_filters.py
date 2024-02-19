from django import template
import json

register = template.Library()

@register.filter(name='get_range')
def get_range(value):
    return range(1, value + 1)

import random

@register.filter(name='random_color')
def random_color(value):
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


@register.filter(name='random_neutral_color')
def random_neutral_color(value):
    shades_of_gray = ['#B2BEB5', '#A9A9A9', '#D3D3D3', '#E5E4E2', '#C0C0C0']
    # black_and_white = ['#000000', '#FFFFFF']
    
    # Combine shades of gray, black, and white
    neutral_colors = shades_of_gray
    
    return random.choice(neutral_colors)


@register.filter
def parse_change_message(change_message):
    try:
        change_message_dict = json.loads(change_message)
        parsed_message = ""

        for key, value in change_message_dict.items():
            if key == 'added':
                for field_name, field_value in value.items():
                    parsed_message += f"Added {field_value['name']}: {field_value['object']}<br>"
            elif key == 'changed':
                for field_name in value['fields']:
                    parsed_message += f"Changed {field_name}<br>"

        return parsed_message
    except json.JSONDecodeError:
        return change_message