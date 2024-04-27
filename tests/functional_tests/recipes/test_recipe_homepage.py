# from django.test import LiveServerTestCase
import pytest
from selenium.webdriver.common.by import By
from tests.functional_tests.base import RecipeBaseFunctionalBase


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalBase):
    def test_recipe_homepage_without_recipes_not_found_message(self):
        self.browser.get(f'{self.live_server_url}/')
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)
