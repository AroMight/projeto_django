from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Recipe, Category
from recipes.serializers import RecipeSerializer, CategorySerializer


@api_view(['GET'])
def recipe_api_list(request):
    recipes = Recipe.objects.filter(is_published=True).order_by(
        '-id').select_related('category', 'author')[:10]
    serializer = RecipeSerializer(
        instance=recipes,
        many=True,
        context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def recipe_api_detail(request, id):
    # recipes = get_object_or_404(Recipe.objects.filter(id=pk))
    # serializer = RecipeSerializer(instance=recipes)
    # return Response(serializer.data)
    recipe = Recipe.objects.filter(id=id).first()

    if recipe:
        serializer = RecipeSerializer(
            instance=recipe,
            context={'request': request})
        return Response(serializer.data)
    else:
        return Response({'detail': 'Recipe not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def recipe_api_category(request, pk):
    category = Category.objects.filter(id=pk).first()
    if category:
        serializer = CategorySerializer(instance=category)
        return Response(serializer.data)
    else:
        return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
