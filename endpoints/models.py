from django.db import models

class APIEndpoint(models.Model):
    class HTTPMethod(models.TextChoices):
        GET = "GET", "GET"
        POST = "POST", "POST"
        PUT = "PUT", "PUT"
        DELETE = "DELETE", "DELETE"
    name = models.CharField(max_length=200)
    method = models.CharField(max_length=10, choices=HTTPMethod.choices, default=HTTPMethod.GET)
    url = models.URLField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
