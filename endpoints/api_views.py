from rest_framework import permissions, viewsets
from .models import APIEndpoint
from .serializers import APIEndpointSerializer

class APIEndpointViewSet(viewsets.ModelViewSet):
    queryset = APIEndpoint.objects.all()
    serializer_class = APIEndpointSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ("get", "post", "head", "options")

    def get_queryset(self):
        return (
            APIEndpoint.objects.filter(owner=self.request.user)
            .select_related("category")
            .prefetch_related("tags")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
