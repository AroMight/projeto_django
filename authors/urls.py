from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
from django.urls import include

author_api_v2_router = SimpleRouter(trailing_slash=True)
author_api_v2_router.register(
    r'api/v2',
    views.AuthorAPIv2ViewSet,
    basename='author_api_v2',
)

app_name = 'authors'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recipe/new', views.DashboardRecipe.as_view(),
         name='dashboard_recipe_new'),
    path('dashboard/recipe/<int:id>/delete/',
         views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'),
    path('dashboard/recipe/<int:id>/edit',
         views.DashboardRecipe.as_view(), name='dashboard_recipe_edit'),
    path('', include(author_api_v2_router.urls)),
]
