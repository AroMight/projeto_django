from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
import time


class RecipeBaseFunctionalBase(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def sleep(self, seconds=5):
        self.browser.quit()
        time.sleep(seconds)
