from django.urls import resolve, reverse # type: ignore
from django.test import TestCase # type: ignore
from recipes import views
from recipes.models import Category, Recipe, User



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
        self.assertEqual(
            response.status_code,
            404
        )
    
    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='Café da manhã')
        author = User.objects.create_user(
            first_name='User',
            last_name='name',
            username='username',
            password='123456'
        )
        recipe = Recipe.objects.create(
                category = category,
                author = author,
                title = 'Recipe Title',
                description = 'Description',
                slug = 'recipe-slug',
                preparation_time = 10,
                preparation_time_unit = 'minutes',
                servings = 2,
                servings_unit = 'Porções',
                preparation_steps = 'steps',
                preparation_steps_is_html = False,
                is_published = True,
        )
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id':1}))
        self.assertIs(view.func, views.category)

    
    def test_category_view_returns_200_ok(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 200)
    
    def test_category_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertTemplateUsed(response, 'recipes/pages/category.html')
    
    def test_category_return_404_if_no_categories(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(
            response.status_code,
            404
        )
    
    
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id':1}))
        self.assertIs(view.func, views.recipe)
        
    def test_recipe_detail_view_return_404_if_no_recipes(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(
            response.status_code,
            404
        )