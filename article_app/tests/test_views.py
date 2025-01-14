from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class HealthCheckViewTestCase(APITestCase):
    def test_health_check_api(self):
        url = reverse('health-check')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"ok ok"})
