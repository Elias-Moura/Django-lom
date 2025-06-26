
from django.core.exceptions import ValidationError
from django.test import TestCase

from recipes.tests.fixtures import make_recipe


class RecipeCategoryModelTest(TestCase):
    def setUp(self):
        self.recipe = make_recipe()
        return super().setUp()
    
    def test_category__str__is_name_fiels(self):
        self.assertEqual(
            str(self.recipe.category),
            self.recipe.category.name,
            msg='Cartegory string representation must be '
            f'recipe title "{self.recipe.category.name}" but "{str(self.recipe.category)=}" was recived.'
        )
    

    def test_recipe_catory_name_max_length_is_65_chars(self):
        self.recipe.category.name = 'A' * 66
        
        with self.assertRaises(ValidationError):
            self.recipe.category.full_clean()