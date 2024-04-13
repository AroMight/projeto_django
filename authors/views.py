from django.shortcuts import render
from .forms import RegisterForm
from django.http import Http404
from django.shortcuts import redirect

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/pages/register.html', context={
        'title':'Recipe |',
        'form': form,
    })

def register_create(request):
    if not request.POST:
        raise Http404('Page not found')
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    return  redirect('authors:register')
