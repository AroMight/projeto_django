from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
from unittest import skip

class RecipeViewsTest(RecipeTestBase):
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
        self.assertEqual(response_context_recipes.first().is_published, True)
    
    def test_home_view_no_loads_recipe_if_published_is_false(self):
        '''Test that the home view does not load recipes that are not published.'''
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        response_context_recipes = response.context['recipes']
        self.assertEqual(len(response_context_recipes), 0)

    def test_category_view_function(self):
        '''Test that the category view function is correct.'''
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func, views.category)

    def test_category_view_status_code_404(self):
        '''Test that the category view returns a 404 status code when the category does not exist.'''
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_category_view_template(self):
        '''Test that the category view uses the correct template.'''
        self.make_recipe()
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_category_view_loads_recipes(self):
        '''Test that the category view loads recipes from the specified category.'''
        self.make_recipe(title='custom title')
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn('custom title', content)

    def test_category_view_no_loads_recipe_if_published_is_false(self):
        '''Test that the home view does not load recipes that are not published.'''
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_function(self):
        '''Test that the detail view function is correct.'''
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1, 'slug': 'camiseta'})
        )
        self.assertIs(view.func, views.recipe)

    def test_detail_view_status_code_404(self):
        '''Test that the detail view returns a 404 status code when the recipe does not exist.'''
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000, 'slug': 'camiseta'})
        )
        self.assertEqual(response.status_code, 404)

    def test_detail_view_template(self):
        '''Test that the detail view uses the correct template.'''
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1, 'slug': 'camiseta'})
        )
        self.assertTemplateUsed(response, 'recipes/pages/recipe-view.html')

    def test_detail_view_no_loads_recipe_if_published_is_false(self):
        ''''Test that the detail view does not load recipes that are not published.'''
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1, 'slug': 'camiseta'}))
        self.assertEqual(response.status_code, 404)

    def test_search_view_function(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_search_view_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_search_view_status_code_200(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 200)
