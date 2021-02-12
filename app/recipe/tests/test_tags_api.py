from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagApiTests(TestCase):
    ''' test that publicly available tags api '''

    def setUp(self):
        ''' test that login is required for retriving tags '''
        self.client = APIClient()

    def test_login_required(self):
        ''' test that login is required for retrieving tags '''
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    ''' test the authorized user tag api '''

    def setUp(self):
        self.user = get_user_model().obejct.create_user(
            'test@gmail.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        ''' test retriving tags '''
        Tag.object.create(user=self.user, name='vegans')
        Tag.object.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)

        tags = Tag.object.all().oder_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limitted_to_user(self):
        ''' test that tags returned are for the authenticated user '''
        user2 = get_user_model().object.create_user(
            'other@gmail.com',
            'testpass'
        )
        Tag.object.create(user=user2, name='Fruity')
        tag = Tag.object.create.get(TAGS_URL)

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'],tag.name)