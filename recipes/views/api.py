from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from recipes.models import Recipe, Category
from recipes.serializers import RecipeSerializer, CategorySerializer


@api_view(['GET', 'POST'])
def recipe_api_list(request):

    if request.method == 'GET':
        recipes = Recipe.objects.filter(is_published=True).order_by(
            '-id').select_related('category', 'author')[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            category_id=1, author_id=1
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view(['GET', 'PATCH', 'DELETE'])
def recipe_api_detail(request, id):
    # recipes = get_object_or_404(Recipe.objects.filter(id=pk))
    # serializer = RecipeSerializer(instance=recipes)
    # return Response(serializer.data)
    recipe = get_object_or_404(Recipe.objects.filter(id=id))

    if request.method == 'GET':

        serializer = RecipeSerializer(
            instance=recipe,
            context={'request': request})
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(
            category_id=1, author_id=1
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    if request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@ api_view(['GET'])
def recipe_api_category(request, pk):
    category = Category.objects.filter(id=pk).first()
    if category:
        serializer = CategorySerializer(instance=category)
        return Response(serializer.data)
    else:
        return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
