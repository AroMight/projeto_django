from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here 😞</h1>',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='CATEGORY')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            email='username@email.com',
            password='123456',
            )
        recipes = Recipe.objects.create(
            category=category,
            author=author,
            title = 'Recipe Title',
            description = 'Recipe description',
            slug = 'Recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            servings_unit = 'Porções',
            preparation_steps = 'lorem lorem lorem lorem loiremp',
            preparation_step_is_html = False,
            is_published = True,
            cover = 'recipes/covers/2021/10/10/recipe-cover.jpg',
            )
        
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8') #CONTENT É O HTML DA PÁGINA
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe description', content)
        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertEqual(len(response_context_recipes), 1)
        self.assertEqual(response_context_recipes.first().is_published, True)

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1, 'slug':'camiseta'})
        )
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000, 'slug':'camiseta'})
        )
        self.assertEqual(response.status_code, 404)
        
    def test_recipe_view_detail_template_is_correct(self):
        category = Category.objects.create(name='CATEGORY')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            email='username@email.com',
            password='123456',
            )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title = 'Recipe Title',
            description = 'Recipe description',
            slug = 'Recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            servings_unit = 'Porções',
            preparation_steps = 'lorem lorem lorem lorem loiremp',
            preparation_step_is_html = False,
            is_published = True,
            cover = 'recipes/covers/2021/10/10/recipe-cover.jpg',
            )
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id':1, 'slug':'camiseta'})
            )
        self.assertTemplateUsed(response,'recipes/pages/recipe-view.html')
        
    def test_recipe_view_category_temaplate_is_correct(self):
        category = Category.objects.create(name='CATEGORY')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            email='username@email.com',
            password='123456',
            )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title = 'Recipe Title',
            description = 'Recipe description',
            slug = 'Recipe-slug',
            preparation_time = 10,
            preparation_time_unit = 'Minutos',
            servings = 5,
            servings_unit = 'Porções',
            preparation_steps = 'lorem lorem lorem lorem loiremp',
            preparation_step_is_html = False,
            is_published = True,
            cover = 'recipes/covers/2021/10/10/recipe-cover.jpg',
            )
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))

        self.assertTemplateUsed(response,'recipes/pages/category.html')

        #     def test_recipe_home_template_loads_recipes(self):
            # category = Category.objects.create(name='CATEGORY')
            # author = User.objects.create_user(
            #     first_name='user',
            #     last_name='name',
            #     username='username',
            #     email='username@email.com',
            #     password='123456',
            #     )
            # recipe = Recipe.objects.create(
            #     category=category,
            #     author=author,
            #     title = 'Recipe Title',
            #     description = 'Recipe description',
            #     slug = 'Recipe-slug',
            #     preparation_time = 10,
            #     preparation_time_unit = 'Minutos',
            #     servings = 5,
            #     servings_unit = 'Porções',
            #     preparation_steps = 'lorem lorem lorem lorem loiremp',
            #     preparation_step_is_html = False,
            #     is_published = True,
            #     cover = 'recipes/covers/2021/10/10/recipe-cover.jpg',
            #     )
            
            # response = self.client.get(reverse('recipes:home'))
            # self.assertEqual(len(response.context['recipes']), 1)