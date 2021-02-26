from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class WithNoDetails(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """Кастомный ViewSet."""
    pass
