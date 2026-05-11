from rest_framework import permissions, viewsets

from .models import SiteContent
from .serializers import SiteContentSerializer


class SiteContentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SiteContentSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"

    def get_queryset(self):
        queryset = SiteContent.objects.filter(is_published=True).order_by("-updated_at")
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            queryset = SiteContent.objects.all().order_by("-updated_at")
        return queryset
