from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def recipe_api_list(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')[:10]
    serializer = RecipeSerializer(instance=recipes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recipe_api_detail(request, pk):
    # recipes = get_object_or_404(Recipe.objects.filter(id=pk))
    # serializer = RecipeSerializer(instance=recipes)
    # return Response(serializer.data)
    recipes = Recipe.objects.filter(id=pk)

    if recipes:
        serializer = RecipeSerializer(instance=recipes)
        return Response(serializer.data)
    else:
        return Response({'detail': 'Recipe not found.'}, status=status.HTTP_418_IM_A_TEAPOT)
