from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse


class UsersTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        URL = reverse('api:users')
        pyload = {
            "email":"test@test.com",
            "password":"bokuakirada"
        }
        response = self.client.post(path=URL, data=pyload)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_create_user_common_password(self):
        URL = reverse('api:users')
        pyload = {
            "email": "test@test.com",
            "password": "football"
        }

        response = self.client.post(path=URL, data=pyload)
        self.assertEqual(status.HTTP_200_OK,response.status_code)






