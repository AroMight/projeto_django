from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'email',
            ] #ou '__all__'
        # widgets = {
        #     'password': forms.PasswordInput()
        # }

class RegisterRecipe(forms.Form):
    recipe_title = forms.CharField(label='Nome da Receita', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nome da Receita'}))
    preparation_time = forms.IntegerField(label='Tempo de Preparo')
    recipe_img = forms.ImageField(label='Imagem da Receita')