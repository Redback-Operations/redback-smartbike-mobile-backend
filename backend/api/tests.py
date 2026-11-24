from unittest import expectedFailure

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Ported from the old backend's Postman suite (signup/login requests).
# Endpoints that don't exist in this repo yet (workouts, messages, password
# reset, social login, update, delete) are not ported.


class RegisterTests(APITestCase):
    url = reverse("register")
    payload = {"username": "test", "email": "test@test.com", "password": "Sup3r-secret-pw"}

    def test_register_valid(self):
        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "test")
        self.assertEqual(response.data["email"], "test@test.com")
        self.assertIn("id", response.data)
        self.assertNotIn("password", response.data)

    def test_register_hashes_password(self):
        self.client.post(self.url, self.payload)
        user = User.objects.get(username="test")
        self.assertNotEqual(user.password, self.payload["password"])
        self.assertTrue(user.check_password(self.payload["password"]))

    def test_register_missing_username(self):
        response = self.client.post(self.url, {**self.payload, "username": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_register_missing_password(self):
        response = self.client.post(self.url, {"username": "test", "email": "test@test.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_register_duplicate_username(self):
        self.client.post(self.url, self.payload)
        response = self.client.post(self.url, {**self.payload, "email": "other@test.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    # Gap: serializer has no unique-email check (Postman expected 409).
    @expectedFailure
    def test_register_duplicate_email_case_insensitive(self):
        self.client.post(self.url, self.payload)
        response = self.client.post(self.url, {**self.payload, "username": "test2", "email": "TEST@test.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Gap: serializer bypasses AUTH_PASSWORD_VALIDATORS.
    @expectedFailure
    def test_register_weak_password(self):
        response = self.client.post(self.url, {**self.payload, "password": "1"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenTests(APITestCase):
    url = reverse("get_token")
    refresh_url = reverse("refresh")

    def setUp(self):
        User.objects.create_user(username="test", email="test@test.com", password="Sup3r-secret-pw")

    def test_token_valid(self):
        response = self.client.post(self.url, {"username": "test", "password": "Sup3r-secret-pw"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_wrong_password(self):
        response = self.client.post(self.url, {"username": "test", "password": "SUP3R-SECRET-PW"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_unknown_user(self):
        response = self.client.post(self.url, {"username": "nobody", "password": "Sup3r-secret-pw"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_missing_password(self):
        response = self.client.post(self.url, {"username": "test"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_valid(self):
        tokens = self.client.post(self.url, {"username": "test", "password": "Sup3r-secret-pw"}).data
        response = self.client.post(self.refresh_url, {"refresh": tokens["refresh"]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_invalid(self):
        response = self.client.post(self.refresh_url, {"refresh": "not-a-token"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
