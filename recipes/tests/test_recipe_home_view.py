from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_home_view_function(self):
        '''Test that the home view function is correct.'''
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_home_view_status_code_200(self):
        '''Test that the home view returns a 200 status code.'''
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        '''Test that the home view uses the correct template.'''
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_home_view_no_recipes_found(self):
        '''Test that the home view displays a message when no recipes are found.'''
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here 😞</h1>',
            response.content.decode('utf-8')
        )

    def test_home_view_loads_recipes(self):
        '''Test that the home view loads recipes that are published.'''
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_context_recipes), 1)
        self.assertEqual(response_context_recipes.object_list[0].is_published, True)
    
    def test_home_view_no_loads_recipe_if_published_is_false(self):
        '''Test that the home view does not load recipes that are not published.'''
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes']
        self.assertEqual(len(response_context_recipes), 0)

    
    def test_home_view_returns_page_1_if_page_not_int(self):
        self.make_recipe()
        self.make_recipe(title='2', slug='two', author_data={'username': 'Luciane'})
        self.make_recipe(title='3', slug='three',author_data={'username': 'Denilson'})
        self.make_recipe(title='4', slug='four',author_data={'username': 'natan'})
        self.make_recipe(title='5', slug='five',author_data={'username': 'davi'})
        self.make_recipe(title='6', slug='six',author_data={'username': 'kelly'})
        self.make_recipe(title='7', slug='seve',author_data={'username': 'fabricio'})
        self.make_recipe(title='8', slug='eig',author_data={'username': 'amanda'})
        self.make_recipe(title='9', slug='nine',author_data={'username': 'amarildo'})
        self.make_recipe(title='10', slug='teen',author_data={'username': 'adeilson'})
        self.make_recipe(title='11', slug='eleve',author_data={'username': 'thalia'})
        self.make_recipe(title='12', slug='twelve',author_data={'username': 'briuno'})
        self.make_recipe(title='13', slug='thirty',author_data={'username': 'danilo'})
        self.make_recipe(title='14', slug='foruty',author_data={'username': 'nairtoin'})
        self.make_recipe(title='15', slug='fifity',author_data={'username': 'miller'})
        self.make_recipe(title='16', slug='sixty',author_data={'username': 'guuh'})
        url = reverse('recipes:home')
        response = self.client.get(f'{url}?page=not_int')
        response_context_recipes = response.context['recipes']
        self.assertEqual(len(response_context_recipes), 9)