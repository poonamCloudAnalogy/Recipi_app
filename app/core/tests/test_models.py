from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='test123'):
    ''' create a sample user '''
    return get_user_model().object.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_succesful(self):
        email = 'test45@gmail.com'
        password = 'testpass123'
        user = get_user_model().object.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'testj@GMAIL.COM'
        user = get_user_model().object.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email error"""
        with self.assertRaises(ValueError):
            get_user_model().object.create_user(None, 'test123')

    def test_create_new_superuser(self):
        user = get_user_model().object.create_superuser(
            'teshhjt@gmail.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        ''' test the tag string representation '''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)
    

    def test_ingredient_str(self):
        """ Test the ingredient string represntation """
        ingrediant = models.Ingredient.objects.create(
        user=sample_user(),
        name='Cucumber'
        )
        self.assertEqual(str(ingrediant),ingrediant.name)

    def test_recipe_str(self):
        """ test the recipe string representation """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='steak and mushroom souce',
            time_minutes=5,
            price=5.60
        )

        self.assertEqual(str(recipe),recipe.title)
        