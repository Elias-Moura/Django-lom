from django.urls import resolve, reverse  # type: ignore
from django.test import TestCase  # type: ignore
from recipes import views
from recipes.tests.fixtures import make_recipe




class RecipeViewsTest(TestCase):
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
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

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

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
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
    
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'
        
        make_recipe(title=needed_title)
        response = self.client.get(
            reverse(
                'recipes:recipe', 
                kwargs={'id':1}
                )
            )
        
        content = response.content.decode('utf-8')
        
        self.assertIn(
            needed_title,
            content
        )
        
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test if recipe is_published false dont show"""
        
        make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_category_template_returns_404_if_no_recipe_published(self):
        
        make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertEqual(
            response.status_code,
            404
        )
        
    
    def test_category_template_returns_404_if_no_recipes_published(self):
        
        make_recipe(is_published=False)
        
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(
            response.status_code,
            404
        )