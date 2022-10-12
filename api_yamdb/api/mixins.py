from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet

from .permissions import IsAdminOrReadOnly


class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
