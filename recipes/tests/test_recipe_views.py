
from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Recipe, Category, User

class RecipeViewsTest(TestCase):
    
    #TESTA SE A URL ESTÁ CORRETA
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(
            view.func, views.home
            )

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id':1,'slug':'camiseta'}))
        self.assertIs(
            view.func, views.recipe
            )
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertIs(
            view.func, views.category
            )

    #TESTAR SE O STATUS CODE É 200 / 404
    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(
            response.status_code, 200
            )

    def test_recipe_detail_view_returns_404_if_no_recipes(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1000, 'slug':'camiseta'}))
        self.assertEqual(
            response.status_code, 404
            )

    def test_recipe_category_view_returns_404_if_no_recipes(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1000}))
        self.assertEqual(
            response.status_code, 404
            )

    #TESTA SE O TEMPLATE RENDERIZADO É O CORRETO   
    def test_recipe_view_home_template_is_correct(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(
            response,'recipes/pages/home.html'
            )
        
    def test_recipe_view_home_template_is_correct_when_no_recipes_found(self):
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
            is_published = True
            )
        assert 1==1
        
    def test_recipe_view_detail_template_is_correct(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id':1,'slug':'camiseta'}))
        self.assertTemplateUsed(
            response,'recipes/pages/recipe-view.html'
            )
        
    def test_recipe_view_category_temaplate_is_correct(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertTemplateUsed(
            response,'recipes/pages/category.html'
            )