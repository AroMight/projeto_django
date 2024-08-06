from collections import defaultdict
from django.forms import ValidationError
from django.contrib.auth.models import User


class AuthorsRegisterValidator:

    def __init__(self, data, errors=None, ErrorClass=None):
        self.cleaned_data = data
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.clean()

    def clean(self, *args, **kwargs):
        self.clean_email()

        cd = self.cleaned_data

        password = cd.get('password')
        password2 = cd.get('password2')

        if password != password2:
            self.errors['password'].append(
                'Password and password2 must be equal')
            self.errors['password2'].append(
                'Password and password2 must be equal')
        if self.errors:
            raise self.ErrorClass(self.errors)

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            self.errors['email'].append('User e-mail is already in use')

        return email
