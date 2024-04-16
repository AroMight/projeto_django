from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from .forms import RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    try:
        del request.session['register_form_data']
    except KeyError:
        pass

    return render(request, 'authors/pages/register.html', context={
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
    else:
        request.session['register_form_data'] = POST

    return redirect('authors:register')
