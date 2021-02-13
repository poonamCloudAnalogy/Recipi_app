from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


def sample_recipe(user, **params):
    """ create and return a sample recipe """
    defaults = {
        'title': 'sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }
    defaults.update(params)

    return Recipe.objects.create(user, **defaults)


class PublicRecipeApiTests(TestCase):
    """ test unauthenticated recipe api access """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ test that authentication is required """
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """ test authentication recipe api access """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            'test@gamil.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """ test retriveing a list of recipes """

        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipe = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipe, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_recipies_limited_to_user(self):
        """ test retriving recipes for user """
        user2=get_user_model.object.create_user(
            'other@gmail.com',
            'testpass'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)

        recipes=Recipe.objects.filter(user=self.user)
        serializer =RecipeSerializer(recipes,many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data,serializer.data)
