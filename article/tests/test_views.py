from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class HelloAPIViewTestCase(APITestCase):
    def test_hello_api(self):
        url = reverse('hello-api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"Hello"})
