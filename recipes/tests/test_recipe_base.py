from django.test import TestCase
from recipes.models import Category, Recipe, User

class RecipeTestBase(TestCase):
    def setUp(self):
        super().setUp()
        
    def make_category(self, name='CATEGORY'):
        return Category.objects.create(name=name)
    
    def make_author(self, first_name='user', last_name='name', username='username', password='123456'):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
        )
    
    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe description',
        slug='Recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        preparation_steps='lorem lorem lorem lorem loiremp',
        preparation_step_is_html=False,
        is_published=True,
        cover='recipes/covers/2021/10/10/recipe-cover.jpg',
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category = self.make_category(**category_data),
            author = self.make_author(**author_data),
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
            cover=cover,
        )        