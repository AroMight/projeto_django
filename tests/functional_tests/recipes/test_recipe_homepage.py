# from django.test import LiveServerTestCase
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tests.functional_tests.base import RecipeBaseFunctionalBase
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalBase):
    def test_recipe_homepage_without_recipes_not_found_message(self):
        self.browser.get(f'{self.live_server_url}/')
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=9)

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # clica neste input e digita o termo de busca
        # para encontrar a receita com o título desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # o usuário vê o que estava procurando
        self.assertIn(title_needed, self.browser.page_source)

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_homepage_pagination(self):
        recipes = self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 3)
