from rest_framework import serializers
from recipes.models import Category, User


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=65)


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all())
    category_name = serializers.StringRelatedField(source='category')
    category_link = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='recipes:recipe_api_v2_category',
        lookup_field='pk',
        source='category',
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    author_name = serializers.StringRelatedField(source='author')

    def get_preparation(self, obj):
        """Returns the preparation time and unit."""
        return {'preparation time': obj.preparation_time,
                'preparation time unit': obj.preparation_time_unit}
    # class Meta:
    #     model = Recipe
    #     fields = ['id', 'title', 'description', 'preparation_time',]
    #     extra_kwargs = {
    #         'title': {'required': True},
    #     }
