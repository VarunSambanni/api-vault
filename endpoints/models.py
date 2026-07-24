from django.db import models
from django.conf import settings
from django.db import models

class Category(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(fields=("owner", "name"), name ="unique_category_name_per_owner")
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(fields=("owner", "name"), name="unique_tag_name_per_owner")
        ]

    def __str__(self):
        return self.name

class APIEndpoint(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="api_endpoints")


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

    headers = models.JSONField(default=dict, blank=True)
    request_body = models.JSONField(default=dict, blank=True)
    sample_response = models.JSONField(default=dict, blank=True)
    is_favorite = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="endpoints",
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="endpoints",
    )

    def __str__(self):
        return self.name
