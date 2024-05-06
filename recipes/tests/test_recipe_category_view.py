from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_category_view_function(self):
        '''Test that the category view function is correct.'''
        view = resolve(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_category_view_status_code_404(self):
        '''Test that the category view returns a 404 status code when the category does not exist.'''
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_category_view_template(self):
        '''Test that the category view uses the correct template.'''
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_category_view_loads_recipes(self):
        '''Test that the category view loads recipes from the specified category.'''
        self.make_recipe(title='custom title')
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        content = response.content.decode('utf-8')
        self.assertIn('custom title', content)

    def test_category_view_no_loads_recipe_if_published_is_false(self):
        '''Test that the home view does not load recipes that are not published.'''
        self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)
