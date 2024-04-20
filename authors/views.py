from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from .forms import RegisterForm
from django.contrib import messages


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register_view.html', context={
        'title': 'Recipe |',
        'form': form,
    })


def register_create(request):
    if not request.POST:
        raise Http404('Page not found')

    POST = request.POST
    form = RegisterForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request, 'User created successfully, please log in.')
        del request.session['register_form_data']

    else:
        request.session['register_form_data'] = POST

    return redirect('authors:register')
