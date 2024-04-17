from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    '''Add an attribute (generic) to the field.'''
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placecholder(field, placeholder_val):
    '''Add a placeholder to the field.'''
    add_attr(field, 'placeholder', placeholder_val)


def add_autocomplete_off(field):
    '''Remove the autocomplete feature from the field.'''
    add_attr(field, 'autocomplete', 'off')


class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placecholder(self.fields['username'], 'Your first name')
        add_placecholder(self.fields['email'], 'Your email')
        add_placecholder(self.fields['first_name'], 'Ex: John')
        add_placecholder(self.fields['last_name'], 'Ex: Doe')
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
        )
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

    # def clean_password2(self):
    #     '''Check if the passwords match.'''
    #     data1 = self.cleaned_data.get('password')
    #     data2 = self.cleaned_data.get('password2')

    #     if data2 != data1:
    #         raise ValidationError(
    #             'As senhas devem coincidir',
    #             code='invalid',
    #         )

    #     return data2

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
