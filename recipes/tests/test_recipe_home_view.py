from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.tests.fixtures import make_recipe


class RecipeHomeViewTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_temple_shows_no_recipess_found_if_no_rescipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        make_recipe()
        response = self.client.get(reverse('recipes:home'))
        
        self.assertIn(
            'Recipe Title',
            response.content.decode('utf-8')
        )
    
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test if recipe is_published false dont show"""
        
        make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )