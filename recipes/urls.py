from django.urls import include, path
from . import views
from rest_framework.routers import SimpleRouter


app_name = 'recipes'

recipe_api_v2_router = SimpleRouter(
    trailing_slash=True
)

recipe_api_v2_router.register(
    r'',
    views.RecipeAPIv2ViewSet,
    basename='recipe_api_v2',
)


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

    # API Urls
    # path(
    #     'recipes/api/v2/',
    #     views.RecipeAPIv2ViewSet.as_view({
    #         "get": "list",
    #         "post": "create",
    #     }),
    #     name='recipe_api_v2',
    # ),

    # path(
    #     'recipes/api/v2/<int:id>',
    #     views.RecipeAPIv2ViewSet.as_view({
    #         "get": "retrieve",
    #         "patch": "partial_update",
    #         "delete": "destroy",
    #     }),
    #     name='recipe_api_v2_detail',
    # ),

    path(
        'recipes/api/v2/category/<int:pk>',
        views.recipe_api_category,
        name='recipe_api_v2_category',
    ),
    path('recipes/api/v2/', include(recipe_api_v2_router.urls)),
]

# urlpatterns += recipe_api_v2_router.urls
