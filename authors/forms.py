from django import forms
from django.contrib.auth.models import User


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
            'placeholder': 'Repeat your password',
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
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


class RegisterRecipe(forms.Form):
    recipe_title = forms.CharField(label='Nome da Receita', max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Nome da Receita'}))
    preparation_time = forms.IntegerField(
        label='Tempo de Preparo', required=True)
    recipe_img = forms.ImageField(label='Imagem da Receita')
