from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from unittest import skip
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    # executa antes de cada teste
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_with_no_defaults(self):
        recipe = Recipe(category=self.make_category(name='Test Default Category'),
                        author=self.make_author(
                            username='test_default_author'),
                        title='Recipe Title',
                        description='Recipe description',
                        slug='recipe-slug',
                        preparation_time=10,
                        preparation_time_unit='Minutos',
                        servings=5,
                        servings_unit='Porções',
                        preparation_steps='lorem lorem lorem lorem loiremp',
                        cover='recipes/covers/2021/10/10/recipe-cover.jpg',
                        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('preparation_step_is_html', False),
        ('is_published', False),
    ])
    def test_recipe_default_values(self, field, default_value):
        '''Test that the recipe fields have the correct default values.'''
        recipe = self.make_recipe_with_no_defaults()
        self.assertEqual(
            getattr(recipe, field),
            default_value,
            msg=f"Recipe {field} should be {default_value} by default."
        )

    def test_if_str_method_returns_recipe_title(self):
        '''Test that the __str__ method returns the recipe title.'''
        self.recipe.title = 'Recipe Title'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Recipe Title')
