from rest_framework import (
    viewsets, filters, status, mixins
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.core.exceptions import ObjectDoesNotExist
from titles.models import Title, Genre, Category, Review, GenreTitle
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
    permission_classes = [IsAdministratorOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    lookup_field = 'id'
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def retrieve(self, request, *args, **kwargs):
        instance = Title.objects.get(id=self.kwargs.get('id'))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    """
    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        
        data['genre'] = GenreSerializer(
            Genre.objects.filter(slug__in=data['genre']), many=True
        ).data
        data['category'] = CategorySerializer(
            Category.objects.filter(slug__in=data['category'])[0]
        ).data
        
        serializer = self.get_serializer(data=request.data)
        print(11111111111)
        serializer.is_valid(raise_exception=True)
        print(2222222222222)
        self.perform_create(serializer)
        print(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    """

    def perform_create(self, serializer):
        data = dict(self.request.data)
        if 'category' not in data or 'genre' not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            print(4444444)
            print(data['category'])
            category_slug = data['category'][0] if isinstance(data['category'], list) else data['category']
            serializer.save(
                genre=Genre.objects.filter(slug__in=data['genre']),
                category=Category.objects.get(slug=category_slug)
            )
        except ObjectDoesNotExist:
            print(5555555555)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_update(self, serializer):
        data = dict(self.request.data)
        if 'category' not in data or 'genre' not in data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            serializer.save(
                genre=Genre.objects.filter(slug__in=data['genre']),
                category=Category.objects.get(slug=data['category'])
            )
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


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

