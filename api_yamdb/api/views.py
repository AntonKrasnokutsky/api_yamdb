from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from titles.models import Title, Genre, Category, Review
from .serializers import (
    TitleSerializer, GenreSerializer, CategorySerializer,
    ReviewSerializer, CommentSerializer,
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
    serializer_class = CategorySerializer
    #permission_classes = None


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (автор, модератор, админ, суперадмин)

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


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (автор, модератор, админ, суперадмин)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    # def get_permissions(self):
    #     if self.action == 'retrieve':
    #         return (ReadOnly(),)
    #     return super().get_permissions()

    def perform_create(self, serializer):
        if not serializer.is_valid():
            return super().permission_denied(self.request)
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
