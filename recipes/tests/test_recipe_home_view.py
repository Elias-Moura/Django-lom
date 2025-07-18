from unittest.mock import patch
from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.tests.fixtures import make_many_recipes, make_recipe


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
        
    @patch('recipes.views.ITENS_PER_PAGE', new=9)
    def test_recipe_home_is_paginated(self):
        make_many_recipes(18)
        
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        paginator = recipes.paginator
        
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 9)
        self.assertEqual(len(paginator.get_page(2)), 9)
    
    
    @patch('recipes.views.ITENS_PER_PAGE', new=3)
    def test_invalid_page_query_uses_page_one(self):
        make_many_recipes(8)
        
        response = self.client.get(reverse('recipes:home') + '?page=1A')
        
        self.assertEqual(
            response.context['recipes'].number,
            1
        )
        
        response = self.client.get(reverse('recipes:home') + '?page=2')
        
        self.assertEqual(
            response.context['recipes'].number,
            2
        )