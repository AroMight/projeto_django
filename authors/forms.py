from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    '''Add an attribute (generic) to the field.'''
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    '''Add a placeholder to the field.'''
    add_attr(field, 'placeholder', placeholder_val)


def add_autocomplete_off(field):
    '''Remove the autocomplete feature from the field.'''
    add_attr(field, 'autocomplete', 'off')


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(('Password must have at least one uppercase letter, '
                               'one lowercase letter and one number. The length should be '
                               'at least 8 characters.'),
                              code='Invalid')


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your first name')
        add_placeholder(self.fields['email'], 'Your email')
        add_placeholder(self.fields['first_name'], 'Ex: John')
        add_placeholder(self.fields['last_name'], 'Ex: Doe')
        add_attr(self.fields['username'], 'css', 'a-css-class')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password]
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model = User
        # ou exclude = ['password']
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'email',
        ]
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'password': 'Password',
        }

        help_texts = {
            'email': 'Enter a valid email address.',
            'last_name': 'Please, submit your last name'
        }

        # required, invalid, max_length, min_length
        error_messages = {
            'username': {
                'required': 'This field is required.',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
                'class': 'input text-input'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here'
            })
        }

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })


# class RecipeForm(forms.Form):
#     title = forms.CharField(max_length=100, required=True, label='Título',
#                             widget=forms.TextInput)

#     password = forms.CharField(max_length=8, widget=forms.PasswordInput(
#         attrs={'placeholder': 'insira uma senha'}))

#     email = forms.EmailField(required=False, widget=forms.URLInput())

#     homem = forms.BooleanField()

#     CHOICES = {"1": "First", "2": "Second"}
#     genero = forms.ChoiceField(
#         widget=forms.SelectMultiple(attrs={'class': 'nt-5'}), choices=CHOICES
#     )

#     null_bolean_field = forms.BooleanField(widget=forms.NullBooleanSelect)

#     radio_field = forms.ChoiceField(label='Campo de radio',
#                                     widget=forms.CheckboxSelectMultiple, choices=({'1': 'opção um', '2': 'opção dois'}))

#     ClearableFile = forms.FileField(
#         required=False, widget=forms.ClearableFileInput)

#     Date_field = forms.DateTimeField(help_text='Digite seu nome completo', error_messages={'invalid': 'OI'},
#                                      widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
