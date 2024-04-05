from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError

class CategoryModeltest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category()
        return super().setUp()


    def tests_if_category_raises_error_if_length_is_more_than_65_caracters(self):
        '''Test that the category name raises an error if it has more than 65 caracters.'''
        self.category.name = 'a' * 66
        with self.assertRaises(ValidationError, msg="The field name can't have more than 65 caracters."):
            self.category.full_clean()

    def tests_if_str_method_returns_name(self):
        '''Test that the category str method returns the category name.'''
        self.category.name ='Category name'
        self.assertEqual(str(self.category),'Category name')