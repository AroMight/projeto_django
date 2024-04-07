from .models import Recipe
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    recipes = Recipe.objects.filter(
            is_published=True
            ).order_by('-id')
    
    current_page = request.GET.get('page', 1)
    paginator = Paginator(recipes, 2)
    page_obj = paginator.get_page(current_page)

    return render(request,'recipes/pages/home.html', context={
        'recipes': page_obj,
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
    search_term = request.GET.get('q','').strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term) |
            Q(category__name__icontains=search_term)
        ),
        is_published=True,
        ).order_by('-id')

    return render(request, 'recipes/pages/search-page.html', context={
        'page_title': f'Buscando por: {search_term} | Delícipedia',
        'search_term': search_term,
        'recipes': recipes,
    })