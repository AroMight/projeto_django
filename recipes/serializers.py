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
            'category_link', 'author', 'author_name',
            'preparation_time_unit', 'preparation_time', 'servings',
            'servings_unit', 'cover', 'preparation_steps',
        ]

    preparation_time_unit = serializers.CharField(write_only=True)

    preparation_time = serializers.IntegerField(write_only=True)

    preparation_steps = serializers.CharField(write_only=True)

    author_name = serializers.StringRelatedField(
        read_only=True,
        source='author',
    )

    public = serializers.BooleanField(
        source='is_published',
        read_only=True
    )

    preparation = serializers.SerializerMethodField(read_only=True)

    category_name = serializers.StringRelatedField(
        source='category',
        read_only=True,
    )

    category_link = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='recipes:recipe_api_v2_category',
        lookup_field='pk',
        source='category',
    )

    def get_preparation(self, obj):
        """Returns the preparation time and unit."""
        return {'preparation time': obj.preparation_time,
                'preparation time unit': obj.preparation_time_unit,
                'preparation steps': obj.preparation_steps}

    # def get_author(self, obj):
    #     return {'author_id': obj.author_id,
    #             'author_name': obj.author_username}

    # def validate_title(self, value):
    #     if len(value) < 5:
    #         raise serializers.ValidationError(
    #             'Title must be at least 5 characters long.')
    #     return value

    def validate(self, data):
        if self.instance is not None and data.get('servings') is None:
            data['servings'] = self.instance.servings

        if self.instance is not None and data.get('preparation_time') is None:
            data['preparation_time'] = self.instance.preparation_time

        if self.instance is not None and data.get('title') is None:
            data['title'] = self.instance.title

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
