from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name='home'),
    path('recipe/search/', views.RecipeListViewSearch.as_view(), name='search'),
    path('recipe/<int:id>/<slug:slug>/',
         views.RecipeDetail.as_view(), name='recipe'),
    path('recipe/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(), name='category'),
]
