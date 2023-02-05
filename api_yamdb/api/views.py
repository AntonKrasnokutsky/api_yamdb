from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from titles.models import Title, Genre, Category, Review
from .serializers import (
    TitleSerializer, GenreSerializer, CategorySerializer,
    ReviewSerializer,
)
from .permissions import (
    IsUserOrReadOnly, IsModeratorOrReadOnly,
    IsAdministratorOrReadOnly, IsSuperUserOrReadOnly
)


class TittleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdministratorOrReadOnly,]
    pagination_class = LimitOffsetPagination
    lookup_field = 'id'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdministratorOrReadOnly,]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        instance = Genre.objects.get(slug=self.kwargs.get('slug'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdministratorOrReadOnly,]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsUserOrReadOnly, IsModeratorOrReadOnly,
        IsAdministratorOrReadOnly, IsSuperUserOrReadOnly
    )

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        return Review.objects.filter(title=title_id)

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return (только_чтение(),)
    #     return super().get_permissions()

    def perform_create(self, serializer):
        if not serializer.is_valid():
            return super().permission_denied(self.request)
        title = Title.objects.get(pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)

