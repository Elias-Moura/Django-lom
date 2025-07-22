from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.tests.fixtures import make_recipe


class RecipeCategoryViewTest(TestCase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_category_view_returns_200_ok(self):
        make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_category_view_loads_correct_template(self):
        make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'recipes/pages/category.html')

    def test_category_return_404_if_no_categories(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(
            response.status_code,
            404
        )

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category title'
        
        make_recipe(title=needed_title)
        response = self.client.get(
            reverse(
                'recipes:category',
                kwargs={'category_id':1}
                )
            )
        content = response.content.decode('utf-8')
        
        self.assertIn(
            needed_title,
            content
        )
    
    def test_category_template_returns_404_if_no_recipes_published(self):
        
        make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(
            response.status_code,
            404
        )
        
    def test_recipe_category_template_returns_404_if_no_recipe_published(self):
        
        make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertEqual(
            response.status_code,
            404
        )