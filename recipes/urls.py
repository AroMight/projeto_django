from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipes/api/v1', views.RecipeListViewHomeApi.as_view(),
         name='recipes_api_v1'),
    path('recipe/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipe/<int:id>/<slug:slug>/',
         views.RecipeDetail.as_view(), name='recipe'),
    path('recipes/api/v1/<int:id>/<slug:slug>/',
         views.RecipeDetailApi.as_view(), name='recipes_api_v1_detail'),
    path('recipe/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(), name='category'),
]
