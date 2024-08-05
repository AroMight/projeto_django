from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.shortcuts import get_object_or_404
from recipes.models import Recipe, Category
from recipes.serializers import RecipeSerializer, CategorySerializer
from ..permissions import IsOwner


class RecipeAPIv2Pagination(PageNumberPagination):
    page_size = 5


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.all().order_by(
        '-id').select_related('category', 'author')
    http_method_names = ['get', 'post', 'patch', 'delete', 'options', 'head']
    serializer_class = RecipeSerializer
    lookup_field = 'id'
    pagination_class = RecipeAPIv2Pagination
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    def get_object(self):
        pk = self.kwargs.get('id')
        obj = get_object_or_404(self.get_queryset(), pk=pk)

        self.check_object_permissions(self.request, obj)

        return obj

    def get_queryset(self):
        qs = super().get_queryset()

        category_id = self.request.query_params.get('category_id', '')

        if category_id != '' and category_id.isnumeric():
            qs = qs.filter(category_id=category_id)

        return qs

    def create(self, request, *args, **kwargs):
        # request.data['author'] = request.user
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    # exemplo de sobrescrita de metodo
    def partial_update(self, request, *args, **kwargs):
        id = kwargs.get('id')
        recipe = self.get_object()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
            context={'request': request},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            category_id=1,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsOwner()]
        if self.request.method == 'POST':
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()

# Extras


class RecipeAPIV2List(ListCreateAPIView):

    queryset = Recipe.objects.filter(is_published=True).order_by(
        '-id').select_related('category', 'author')

    serializer_class = RecipeSerializer

    pagination_class = RecipeAPIv2Pagination


class RecipeAPIV2Detail(RetrieveUpdateDestroyAPIView):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'id'

    # exemplo de sobrescrita de metodo
    def partial_update(self, request, *args, **kwargs):
        id = kwargs.get('id')
        recipe = self.get_queryset().filter(id=id).first()
        serializer = RecipeSerializer(
            instance=recipe,
            data=request.data,
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


# class RecipeAPIV2Detail(APIView):

#     def get_recipe(self, id):
#         recipe = get_object_or_404(Recipe.objects.filter(id=id))

#         return recipe

#     def get(self, request, id):

#         recipe = self.get_recipe(id)
#         serializer = RecipeSerializer(
#             instance=recipe,
#             context={'request': request}
#         )
#         return Response(serializer.data)

#     def patch(self, request, id):
#         recipe = self.get_recipe(id)
#         serializer = RecipeSerializer(
#             instance=recipe,
#             data=request.data,
#             many=False,
#             context={'request': request},
#             partial=True,
#         )

#         serializer.is_valid(raise_exception=True)
#         serializer.save(
#             category_id=1, author_id=1
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK
#         )

#     def delete(self, request, id):
#         recipe = self.get_recipe(id)
#         recipe.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


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
