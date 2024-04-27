import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from recipes.tests.test_recipe_base import RecipeMixing
from utils.browser import make_chrome_browser


class RecipeBaseFunctionalBase(StaticLiveServerTestCase, RecipeMixing):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def sleep(self, seconds=5):
        time.sleep(seconds)
