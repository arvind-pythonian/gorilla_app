from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


user_data = {
    "username": "admin",
    "first_name": "admin",
    "last_name": "super",
    "email": "admin@gmail.com",
    "mobile_number": "9874563211",
    "password": "Admin@2025"
}

class AccountTests(APITestCase):
    def test_create_account(self):
        url = reverse('sign_up')
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login(self):
        url = reverse('sign_up')
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('token_obtain_pair')
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)