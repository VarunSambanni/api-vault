from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import APIEndpoint

class EndpointListTests(TestCase):
    def setUp(self):
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username="owner",
            password="test-password-123",
        )

        self.other_user = user_model.objects.create_user(
            username="other-owner",
            password="test-password-123",
        )

        self.own_endpoint = APIEndpoint.objects.create(
            owner=self.user,
            name="My endpoint",
            method="GET",
            url="https://example.com/my-endpoint",
        )

        self.other_endpoint = APIEndpoint.objects.create(
            owner=self.other_user,
            name="Someone else's endpoint",
            method="GET",
            url="https://example.com/other-endpoint",
        )

    def test_login_is_required(self):
        list_url = reverse("endpoints:endpoint-list")
        response = self.client.get(list_url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={list_url}",
        )

    def test_list_only_shows_the_users_endpoints(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("endpoints:endpoint-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.own_endpoint.name)
        self.assertNotContains(response, self.other_endpoint.name)