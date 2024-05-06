import os
from django.db.models import Q
from django.http import Http404
from django.views.generic import ListView, DetailView
from utils.pagination import make_pagination
from .models import Recipe


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    # paginate_by = None
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = ''

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        ctx.update({'recipes': page_obj, 'pagination_range': pagination_range})

        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        category_id = self.kwargs.get('category_id')
        qs = super().get_queryset(*args, **kwargs)

        if not qs:
            raise Http404

        qs = qs.filter(category__id=category_id)
        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search-page.html'

    def get_search_term(self):
        search_term = self.request.GET.get('q', '').strip()
        return search_term

    def get_queryset(self, *args, **kwargs):
        search_term = self.get_search_term()
        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term),
        ),
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({'search_term': search_term,
                    'additional_url_query': f'&q={search_term}',
                    'page_title': f'Buscando por: "{search_term}" |'})

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'
    pk_url_kwarg = "id"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({'is_detail_page': True,
                    'page_title': f'{self.object.title} |'})

        return ctx
