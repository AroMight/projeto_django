from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'recipes/home.html', context={
        'name': 'Denilson', 'idade':'30'
    })

def contact(request):
    return HttpResponse('CONTATOS')

def about(request):
    return HttpResponse('SOBRE')

# Create your views here.
