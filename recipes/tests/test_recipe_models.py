from django.core.exceptions import ValidationError
from django.test import TestCase
from parameterized import parameterized

from recipes.models import Recipe
from recipes.tests.fixtures import make_author, make_category, make_recipe


class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = make_recipe()
        return super().setUp()
    

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=make_category(name='Test Default Category'),
            author=make_author(username='newUsername'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-1',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        
        recipe.full_clean()
        recipe.save()
        
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):

        setattr(self.recipe, field, 'A' * (max_length + 1))

        self.assertRaises(
            ValidationError,
            self.recipe.full_clean
        )

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_stets_is_html is not False'
        )
        
        
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False'
        )
    
    def test_recipe__str__(self):
        self.assertEqual(
            str(self.recipe),
            self.recipe.title,
            msg='Recipe string representation must be ' 
            f'recipe title "{self.recipe.title=}" but "{str(self.recipe)=}" was recived.'
        )