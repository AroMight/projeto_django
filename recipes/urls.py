from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
     path(
          '',
          views.RecipeListViewHome.as_view(),
          name='home'
          ),
          
     path(
          'recipes/api/v1',
          views.RecipeListViewHomeApi.as_view(),
          name='recipes_api_v1',
          ),

     path(
          'recipe/search/',
          views.RecipeListViewSearch.as_view(),
          name='search',
          ),

     path(
          'recipe/<int:id>/<slug:slug>/',
          views.RecipeDetail.as_view(),
          name='recipe',
          ),

     path(
          'recipe/category/<int:category_id>/',
          views.RecipeListViewCategory.as_view(),
          name='category',
          ),

     #API Urls
     path(
          'recipes/api/v2/',
          views.recipe_api_list,
          name='recipe_api_v2',
          ),

     path(
          'recipes/api/v2/<int:id>',
          views.recipe_api_detail,
          name='recipe_api_v2_detail',
          ),

     path(
          'recipes/api/v2/category/<int:pk>',
          views.recipe_api_category,
          name='recipe_api_v2_category',
          ),
]
