from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import *
from .models import Recipe

def home(request):
    recipes = Recipe.objects.filter(
            is_published=True
            ).order_by('-id')

    return render(request,'recipes/pages/home.html', context={
        'recipes': recipes,
        })

def recipe(request, id, slug):
    recipe = get_object_or_404(Recipe.objects.filter(id=id,is_published=True).order_by('-id'))

    return render(request,'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })


def category(request, category_id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,is_published=True
            ).order_by('-id')
        )
    
    return render(request,'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'Categoria | {recipes[0].category.name}'
    })

def search(request):
    return render(request, 'recipes/pages/search.html')