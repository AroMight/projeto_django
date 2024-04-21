import re
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    '''Add an attribute (generic) to the field.'''
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    '''Add a placeholder to the field.'''
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    '''Check if the password is strong enough.'''
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(('Password must have at least one uppercase letter, '
                               'one lowercase letter and one number. The length should be '
                               'at least 8 characters.'),
                              code='Invalid')
