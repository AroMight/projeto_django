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
        add_placeholder(self.fields['first_name'], 'Ex.: John')
        add_placeholder(self.fields['last_name'], 'Ex: Doe')
        add_placeholder(self.fields['password'], 'Type your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    username = forms.CharField(
        required=True,
        label='Username',
        help_text=(
            'Between 3 and 150 characters. Must have letters, numbers and one of those: @/./+/-/_ only.'
        ),
        error_messages={
            'required': 'This field is required.',
            'min_length': 'Username must have at least 4 characters.',
            'max_length': 'Username must have at most 150 characters.',
        },
        min_length=4, max_length=150
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        required=True,
        label='First Name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        required=True,
        label='Last Name',
        help_text='Please, submit your last name'
    )

    email = forms.EmailField(
        required=True,
        label='Email',
        help_text='Enter a valid email address.',
        error_messages={
            'required': 'Enter a valid email address.',
        }
    )

    password = forms.CharField(
        required=True,
        label='Password',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty.'
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
        label='Password2',
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, repeat your password.'
        },
    )

    class Meta:
        '''Meta class to define the model and fields to be used in the form.'''
        model = User
        # ou exclude = ['password']
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
        ]

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
