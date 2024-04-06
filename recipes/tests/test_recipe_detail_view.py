from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeDeatilViewTest(RecipeTestBase):
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
