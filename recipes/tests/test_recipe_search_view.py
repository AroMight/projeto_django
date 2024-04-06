from django.urls import resolve, reverse
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_search_view_function(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_search_view_template(self):
        url = reverse('recipes:search') + '?q=term'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search-page.html')

    def test_search_view_status_code_200(self):
        url = reverse('recipes:search') + '?q=term'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_search_view_status_code_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_scaped(self):
        url = reverse('recipes:search') + '?q=<term>'
        response = self.client.get(url)
        self.assertIn('Buscando por: &lt;term&gt;', response.content.decode('utf-8'))

    def test_recipe_search_can_find_recipe_by_title(self):
        recipe1 = self.make_recipe(title='This is recipe one',slug='one',author_data={'username': 'Luciane'})
        recipe2 = self.make_recipe(title='This is recipe two',slug='two',author_data={'username': 'Denilson'})

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q=one')
        response2 = self.client.get(f'{search_url}?q=two')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1 and recipe2, response_both.context['recipes'])

    #CRIAR TESTES PARA CTEGORY E DESCRIPTION
