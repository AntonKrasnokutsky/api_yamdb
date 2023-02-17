from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets, filters, status, mixins
)
from django_filters.rest_framework import (
    DjangoFilterBackend, FilterSet,
    CharFilter, NumberFilter
)
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from .exceptions import DubleReview
from reviews.models import Title, Genre, Category, Review, Comment
from .serializers import (
    WriteTitleSerializer, GenreSerializer, CategorySerializer,
    ReviewSerializer, ReadTitleSerializer, CommentSerializer,
)
from .permissions import (
    IsAdministratorOrReadOnly,
)

from users.permissions import AuthorOrReviewerOrReadOnly


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year', lookup_expr='iexact')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TittleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
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
        instance = Title.objects.get(id=self.kwargs.get('id'))
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
        title_id = self.kwargs.get("title_id")
        return Review.objects.filter(title=title_id)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     title = get_object_or_404(Title, pk=kwargs.get("title_id"))
    #     review = Review.objects.filter(title=title, author=request.user).exists()
    #     if review:
    #         return Response("Вы уже добавили обзор на это произведение", status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save(author=self.request.user, title=title)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        # review = Review.objects.get(title=title, author=self.request.user)
        # if review:
        #     return Response("Вы уже добавили обзор на это произведение", status=status.HTTP_400_BAD_REQUEST)
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
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
