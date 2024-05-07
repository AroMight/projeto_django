from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authors.forms import RegisterForm, LoginForm
from django.views.generic import FormView
from recipes.models import Recipe


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'authors/pages/register_view.html'
    success_url = '/authors/login/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(
            self.request, 'User created successfully, please log in.')
        return super().form_valid(form)


def login_view(request):
    '''Display the login form.'''
    form = LoginForm()
    return render(request, 'authors/pages/login.html', context={
        'form': form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    '''Authenticate the user and redirect to login page.'''
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(reverse('authors:dashboard'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Invalid logout request')
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):

    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user,
    )
    return render(request, 'authors/pages/dashboard.html', context={
        'recipes': recipes,
    })
