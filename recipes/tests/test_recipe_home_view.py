from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeHomeViewTest(RecipeTestBase):
    def test_home_view_function(self):
        '''Test that the home view function is correct.'''
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

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
        self.assertEqual(
            response_context_recipes.object_list[0].is_published, True)

    def test_home_view_no_loads_recipe_if_published_is_false(self):
        '''Test that the home view does not load recipes that are not published.'''
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes']
        self.assertEqual(len(response_context_recipes), 0)

    def test_home_view_is_pagineted(self):
        self.make_recipe_in_batch(14)

        with patch('recipes.views.PER_PAGE', new=3):
            url = reverse('recipes:home')
            response = self.client.get(f'{url}?page=not_int')
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 5)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)
            self.assertEqual(len(paginator.get_page(4)), 3)
            self.assertEqual(len(paginator.get_page(5)), 2)
