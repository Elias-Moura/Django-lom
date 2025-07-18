import time
from selenium.webdriver import Chrome, ChromeOptions, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pytest

from recipes.tests.fixtures import make_many_recipes, make_recipe
from unittest.mock import patch

from .base import RecipeBaseFunctionalTest



@pytest.mark.functional_test
class RecipeHomePageFuncionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)

    
    @patch('recipes.views.ITENS_PER_PAGE', new=3)
    def test_search_recipe_is_visible(self):
        self.browser.get(self.live_server_url)
        search = self.browser.find_element(By.CSS_SELECTOR, 'input.search-input')
        self.assertIn('Search for a recipe...', search.get_attribute('placeholder'))


    @patch('recipes.views.ITENS_PER_PAGE', new=3)
    def test_recipe_search_input_can_find_correct_recipe(self):
        recipe_title_needed = 'Batata Frita do MacDonalds'
        make_recipe(title=recipe_title_needed)
        make_many_recipes(6)
        
        # Usuário abre a página
        self.browser.get(self.live_server_url)
        
        # Usuário vê o cambo de busca 
        search = self.browser.find_element(By.CSS_SELECTOR, 'input.search-input')
        
        # Clica no input e digita o termo de busca
        # para encontrar a receita com o título desejado.
        search.click()
        
        search.send_keys(recipe_title_needed)
        search.send_keys(Keys.ENTER)
        
        time.sleep(0.01) # Precisa de um atraso para ele não buscar no html atual antes da pesquisa
        recipes_list_text = self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        
        self.assertIn(
            recipe_title_needed, 
            recipes_list_text
        )


    @patch('recipes.views.ITENS_PER_PAGE', new=3)
    def test_recipe_search_input_can_find_correct_recipe(self):
        recipes = make_many_recipes(30)
        
        # Usuário abre a página
        self.browser.get(self.live_server_url)
        
        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        
        time.sleep(2)
        page2.click()
        
        # Vê que tem mais 3 receitas na página 2        
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            3
        )        
        
        
        