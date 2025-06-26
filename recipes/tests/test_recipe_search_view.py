from django.test import TestCase
from django.urls import resolve, reverse

from recipes.tests.fixtures import make_recipe


class RecipeSearchViewTest(TestCase):

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Teste>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )
    
    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'
        
        recipe_1 = make_recipe(title=title1, slug='one', author_data={'username': 'one'})
        recipe_2 = make_recipe(title=title2, slug='two', author_data={'username': 'two'})
        
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=This')
        
        self.assertIn(recipe_1,response1.context['recipes'])
        self.assertNotIn(recipe_2,response1.context['recipes'])
        
        self.assertIn(recipe_2,response2.context['recipes'])
        self.assertNotIn(recipe_1,response2.context['recipes'])
        
        self.assertIn(recipe_1,response_both.context['recipes'])
        self.assertIn(recipe_2,response_both.context['recipes'])