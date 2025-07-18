# from django.test import LiveServerTestCase # Sem JS e CSS
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # Com JS e CSS
from utils.browser import make_chrome_browser, DEFAULT_OPTIONS


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser(*DEFAULT_OPTIONS)
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
    