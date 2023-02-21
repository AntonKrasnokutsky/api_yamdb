from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets, filters, status, mixins
)
from django_filters.rest_framework import (
    DjangoFilterBackend
)
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title, Genre, Category, Review
from .filters import TitleFilter
from .serializers import (
    WriteTitleSerializer, GenreSerializer, CategorySerializer,
    ReviewSerializer, ReadTitleSerializer, CommentSerializer,
)
from .permissions import (
    IsAdministratorOrReadOnly,
)

from users.permissions import AuthorOrReviewerOrReadOnly


class TittleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = ReadTitleSerializer
    permission_classes = [IsAdministratorOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return self.serializer_class
        return WriteTitleSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset.get(id=self.kwargs.get('id'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class GenreViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdministratorOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        instance = Genre.objects.get(slug=self.kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdministratorOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        instance = Category.objects.get(slug=self.kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        AuthorOrReviewerOrReadOnly,
    )

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        AuthorOrReviewerOrReadOnly,
    )

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Review.objects.get(id=review_id).comments.all()

    def perform_create(self, serializer):
        if not serializer.is_valid():
            return super().permission_denied(self.request)
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
