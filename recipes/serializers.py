from rest_framework import serializers
from recipes.models import Category, Recipe
from authors.validators import AuthorRecipeValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        # read_only_fields = ['created_at', 'updated_at']


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'public',
            'preparation', 'category', 'category_name',
            'category_link', 'author', 'author_name', 'preparation_time_unit',
            'preparation_time', 'servings', 'servings_unit', 'cover',
            'preparation_steps',
        ]

    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.StringRelatedField(
        source='category', read_only=True)
    category_link = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='recipes:recipe_api_v2_category',
        lookup_field='pk',
        source='category',
    )
    author_name = serializers.StringRelatedField(source='author')

    def get_preparation(self, obj):
        """Returns the preparation time and unit."""
        return {'preparation time': obj.preparation_time,
                'preparation time unit': obj.preparation_time_unit}

    # def validate_title(self, value):
    #     if len(value) < 5:
    #         raise serializers.ValidationError(
    #             'Title must be at least 5 characters long.')
    #     return value

    def validate(self, data):
        validate_fields = super().validate(data)
        AuthorRecipeValidator(
            validate_fields,
            ErrorClass=serializers.ValidationError
        )
        # title = validate_fields.get('title')
        # description = validate_fields.get('description')

        # if title == description:
        #     raise serializers.ValidationError(
        #         {
        #             "title": ["Title and description must be different."],
        #             "description": ["Title and description must be different."]
        #         }
        #     )
        return data
