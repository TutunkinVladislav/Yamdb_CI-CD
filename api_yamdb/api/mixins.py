from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminSuperuserOrReadOnly


class CreateDestroyListViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    Кастомный Вьюсет с правами для создания, удаления, получения объектов
    """

    lookup_field = 'slug'
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminSuperuserOrReadOnly,)

    pass
