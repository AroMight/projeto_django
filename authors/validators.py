from django import forms
from recipes.models import Recipe
from utils.strings import is_positive_number
from collections import defaultdict
from django.core.exceptions import ValidationError


class AuthorRecipeValidator:
    def __init__(self, data, errors=None, ErrorClass=None):

        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_title()
        self.clean_preparation_time()
        self.clean_servings()
        cd = self.data

        title = cd.get('title')
        description = cd.get('description')

        if title == description:
            self.errors['title'].append('Cannot be equal to description')
            self.errors['description'].append('Cannot be equal to title')

        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_title(self):
        title = self.data.get('title')

        if len(title) < 5:
            self.errors['title'].append('Must have at least 5 chars.')

        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.data.get(field_name)

        if not is_positive_number(field_value):
            self.errors['preparation_time'].append(
                'Must be greater than 0.')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.data.get(field_name)

        if not is_positive_number(self.data.get('servings')):
            self.errors['servings'].append(
                'Must be greater than 0.')

        return field_value