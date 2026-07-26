from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import APIEndpoint
from unittest.mock import Mock, patch

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

class  EndpointTryTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="owner",
            password="test-password-123",
        )
        self.endpoint = APIEndpoint.objects.create(
            owner=self.user,
            name="Test API",
            method="GET",
            url="https://example.com/api",
            headers={"X-Test": "API Vault"},
        )

    @patch("endpoints.views.requests.request")
    def test_try_endpoint_displays_response(self, mock_request):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {
            "Content-Type": "application/json",
        }
        mock_response.json.return_value = {
            "message": "Success",
        }
        mock_response.elapsed.total_seconds.return_value = 0.125
        mock_request.return_value = mock_response
        self.client.force_login(self.user)

        response = self.client.post(
            reverse(
                "endpoints:endpoint-try",
                args=[self.endpoint.pk],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["try_result"]["status_code"],
            200,
        )
        self.assertEqual(
            response.context["try_result"]["response_time_ms"],
            125.0,
        )
        self.assertContains(response, "Success")

        mock_request.assert_called_once_with(
            method="GET",
            url="https://example.com/api",
            headers={"X-Test": "API Vault"},
            timeout=10,
        )
