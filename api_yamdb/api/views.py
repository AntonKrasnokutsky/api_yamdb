from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from titles.models import Title, Genre, Category
from .serializers import (
    TitleSerializer, GenreSerializer, CategorySerializer
)


class TittleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = None
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = None


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = CategorySerializer
    #permission_classes = None


