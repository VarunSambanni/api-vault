from rest_framework import serializers
from .models import APIEndpoint

class APIEndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIEndpoint
        fields = (
            "id",
            "owner",
            "name",
            "method",
            "url",
            "headers",
            "request_body",
            "sample_response",
            "notes",
            "is_favorite",
            "category",
            "tags",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "owner",
            "category",
            "tags",
            "created_at",
            "updated_at",
        )

    def validate_headers(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError(
                "Headers must be a JSON object."
            )

        return value
